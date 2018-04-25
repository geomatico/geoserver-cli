"""
GeoServer
"""
import requests
import logging
import json
from urllib.parse import urljoin
from geoserver.Workspace import Workspace
from geoserver.Layer import Layer
from geoserver.LayerGroup import LayerGroup
from geoserver.Style import Style


class GeoServer:
    def __init__(self, url, user, password):
        self.base_url = url + "/"
        self.url = urljoin(self.base_url, 'rest/')
        self.user = user
        self.password = password

    def _workspace_from_json(self, ws, namespaces=None):
        if not namespaces:
            namespaces = self._get('namespaces')['namespaces']['namespace']

        f = filter(lambda n: n['name'] == ws['name'], namespaces)
        ns = next(f, None)
        if ns:
            ns = self._get(ns['href'])['namespace']['uri']

        return Workspace(ws['name'], self, ns)

    def get_workspaces(self):
        workspaces = self._get('workspaces')['workspaces']['workspace']
        namespaces = self._get('namespaces')['namespaces']['namespace']
        return list(map(lambda x: self._workspace_from_json(x, namespaces),
                        workspaces))

    def get_workspace(self, name):
        if not name:
            return None
        try:
            json = self._get('workspaces/' + name)
        except IOError as e:
            logging.info(e)
            return None

        workspace = json['workspace']
        return self._workspace_from_json(json['workspace'])

    def get_datastores(self, workspace):
        ws = self.get_workspace(workspace)
        if not ws:
            raise ValueError('Invalid workspace: ' + (workspace or ''))
        return ws.get_datastores()

    def get_datastore(self, name, workspace):
        ws = self.get_workspace(workspace)
        if not ws:
            raise ValueError('Invalid workspace: ' + (workspace or ''))
        return ws.get_datastore(name)

    def _layer_from_json(self, layer):
        name = layer['name']
        layer_info = self._get('layers/' + name)['layer']
        style = self.get_style(layer_info['defaultStyle']['name'])

        res = self._get(layer_info['resource']['href'])
        res_info = next(iter(res.values()))
        ws = self.get_workspace(res_info['namespace']['name'])
        ds = ws.get_datastore(res_info['store']['name'])

        qualifiedName = name if ':' in name else ws.get_name() + ':' + name
        return Layer(qualifiedName, self, style, ds, ws)

    def get_layers(self):
        layers = self._get('layers')['layers']['layer']
        return map(self._layer_from_json, layers)

    def get_layer(self, name):
        if not name:
            return None
        try:
            layer = self._get('layers/' + name)['layer']
            return self._layer_from_json(layer)
        except IOError as e:
            logging.info(e)
            return None

    def _layergroup_from_json(self, layergroup):
        name = layergroup['name']
        layergroup_info = self._get('layergroups/' + name)['layerGroup']
        published = layergroup_info['publishables']['published']
        layersJson = map(lambda l: self._get(l['href'])['layer'], published)
        layers = list(map(self._layer_from_json, layersJson))
        return LayerGroup(name, self, layers)

    def get_layergroups(self):
        layers = self._get('layergroups')['layerGroups']['layerGroup']
        return map(self._layergroup_from_json, layers)

    def get_layergroup(self, name):
        if not name:
            return None
        try:
            layer = self._get('layergroups/' + name)['layerGroup']
            return self._layergroup_from_json(layer)
        except IOError as e:
            logging.info(e)
            return None

    def get_styles(self):
        styles = self._get('styles')['styles']['style']
        return list(map(lambda s: Style(s['name'], self), styles))

    def get_style(self, name):
        try:
            style = self._get('styles/' + name)['style']
            return Style(style['name'], self)
        except IOError as e:
            logging.info(e)
            return None

    def reset(self):
        self._request('reset', method='POST')

    def reload(self):
        self._request('reload', method='POST')

    def fonts(self):
        return self._get('fonts')['fonts']

    def create_workspace(self, name, namespace):
        pass

    def create_style(self, name, sld):
        if not name:
            raise ValueError('Invalid name')

        data = json.dumps({
            'style': {
                'name': name,
                'filename': name + '.sld'
            }
        })
        try:
            self._request(
                'styles', method='POST', expected_code=201,
                headers={'Content-type': 'application/json'}, data=data)
            self._request(
                'styles/' + name, method='PUT', format='', data=sld,
                headers={'Content-type': 'application/vnd.ogc.sld+xml'})
        except OSError as e:
            try:
                self._request('styles/' + name, method='DELETE')
            except OSError as e:
                logging.error(e)
            raise IOError('Cannot add style', e)

    def _get(self, path):
        return self._request(path)

    def _request(self, path,
                 format='.json',
                 method='get',
                 expected_code=200,
                 headers={},
                 data=None):
        url = urljoin(self.url, path)
        if format and not url.endswith(format):
            url = url + format
        f = getattr(requests, method.lower())
        r = f(url, auth=(self.user, self.password), data=data, headers=headers)
        if r.status_code != expected_code:
            msg = ("Cannot perform {} request to {}. Response code is {}"
                   .format(method, url, r.status_code))
            raise IOError(msg)
        if format == '.json':
            try:
                return r.json() if r.text else None
            except json.JSONDecodeError:
                return r.text
        else:
            return r.text
