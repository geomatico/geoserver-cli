"""
GeoServer
"""
import requests
import logging
from urllib.parse import urljoin
from geoserver.Workspace import Workspace
from geoserver.Layer import Layer
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
        try:
            json = self._get('workspaces/' + name)
        except IOError as e:
            logging.info(e)
            return None

        workspace = json['workspace']
        return self._workspace_from_json(json['workspace'])

    def get_datastores(self, workspace):
        pass

    def get_datastore(self, name, workspace=None):
        pass

    def get_layers(self):
        layers = self._get('layers')['layers']['layer']
        ret = []
        for layer in layers:
            name = layer['name']
            layer_info = self._get('layers/' + name)['layer']
            style = self.get_style(layer_info['defaultStyle']['name'])

            res = self._get(layer_info['resource']['href'])
            res_info = next(iter(res.values()))
            ws = self.get_workspace(res_info['namespace']['name'])
            ds = self.get_datastore(res_info['store']['name'])

            qualifiedName = name if ':' in name else ws.get_name() + ':' + name
            ret.append(Layer(qualifiedName, self, style, ds, ws))
        return ret

    def get_layer(self, name):
        pass

    def get_layergroups(self):
        pass

    def get_layergroup(self, name):
        pass

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
        self._post('reset')

    def reload(self):
        self._post('reload')

    def fonts(self):
        return self._get('fonts')['fonts']

    def create_workspace(self, name, namespace):
        pass

    def create_style(self, name, sld):
        pass

    def _get(self, path):
        return self._request_json(path)

    def _post(self, path, data=None):
        return self._request_json(path, method='POST')

    def _request_json(self, path,
                      method='get',
                      expected_code=200,
                      data=None):
        url = urljoin(self.url, path)
        if not url.endswith(".json"):
            url = url + ".json"
        f = getattr(requests, method.lower())
        r = f(url, auth=(self.user, self.password), data=data)
        if r.status_code != expected_code:
            msg = ("Cannot perform {} request to {}. Response code is {}"
                   .format(method, url, r.status_code))
            raise IOError(msg)
        return r.json() if r.text else None
