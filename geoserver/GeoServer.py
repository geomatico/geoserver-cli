"""
GeoServer
"""
import logging
import json
from urllib.parse import urljoin
import requests
from geoserver.Workspace import Workspace
from geoserver.Layer import Layer
from geoserver.LayerGroup import LayerGroup
from geoserver.Style import Style

class GeoServer:
    """
    Main class to manage a GeoServer instance.

    It uses the REST API so authentication is required.

    :param url: URL of the GeoServer instance.
    :param user: user for authentication in the REST API.
    :param pass: password for authentication in the REST API.
    :type url: string
    :type user: string
    :type pass: string
    """
    def __init__(self, url, user, password):
        self.base_url = url + "/"
        self.url = urljoin(self.base_url, 'rest/')
        self.user = user
        self.password = password

    def _workspace_from_json(self, ws, namespaces=None):
        if not namespaces:
            namespaces = self._get('namespaces')['namespaces']['namespace']

        f = filter(lambda n: n['name'] == ws['name'], namespaces)
        namespace = next(f, None)
        if namespace:
            namespace = self._get(namespace['href'])['namespace']['uri']

        return Workspace(ws['name'], self, namespace)

    def get_workspaces(self):
        """
        Get all the workspaces in the GeoServer instance.

        :return: All the workspaces.
        :rtype: List of :class:`geoserver.Workspace`
        :raise: :class:`IOError` if any error occurs while requesting the REST API.
        """
        workspaces = self._get('workspaces')['workspaces']['workspace']
        namespaces = self._get('namespaces')['namespaces']['namespace']
        return list(map(lambda x: self._workspace_from_json(x, namespaces),
                        workspaces))

    def get_workspace(self, name):
        """
        Get a specific workspace.

        :param name: Name of the workspace to get.
        :type name: string
        :return: The required workspace or None if the workspace does not exist.
        :rtype: :class:`geoserver.Workspace`
        :raise: :class:`IOError` if any error occurs while requesting the REST API.
        """
        if not name:
            return None
        try:
            workspace = self._get('workspaces/' + name)
        except IOError as e:
            logging.info(e)
            return None

        return self._workspace_from_json(workspace['workspace'])

    def get_datastores(self, workspace):
        """
        Get all the datastores from all workspaces in the GeoServer instance.

        :return: All the datastores.
        :rtype: List of :class:`geoserver.Datastore`
        :raise: :class:`IOError` if any error occurs while requesting the REST API.
        """
        ws = self.get_workspace(workspace)
        if not ws:
            raise ValueError('Invalid workspace: ' + (workspace or ''))
        return ws.get_datastores()

    def get_datastore(self, name, workspace):
        """
        Get a specific datastore from a workspace.

        :param name: Name of the datastore to get.
        :param workspace: Name of the workspace containing the datastore.
        :type name: string
        :type workspace: string
        :return: The required datastore or None if the datastore does not exist.
        :rtype: :class:`geoserver.Datastore`
        :raise: :class:`IOError` if any error occurs while requesting the REST API.
        """
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

        qualified_name = name if ':' in name else ws.get_name() + ':' + name
        return Layer(qualified_name, self, style, ds, ws)

    def get_layers(self):
        """
        Get all the layers in the GeoServer instance.

        :return: All the layers.
        :rtype: List of :class:`geoserver.Layer`
        :raise: :class:`IOError` if any error occurs while requesting the REST API.
        """
        layers = self._get('layers')['layers']['layer']
        return list(map(self._layer_from_json, layers))

    def get_layer(self, name):
        """
        Get a specific layer.

        :param name: Name of the layer to get.
        :type name: string
        :return: The required layer or None if the layer does not exist.
        :rtype: :class:`geoserver.Layer`
        :raise: :class:`IOError` if any error occurs while requesting the REST API.
        """
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
        layers_json = map(lambda l: self._get(l['href'])['layer'], published)
        layers = list(map(self._layer_from_json, layers_json))
        return LayerGroup(name, self, layers)

    def get_layergroups(self):
        """
        Get all the layer groups in the GeoServer instance.

        :return: All the layer groups.
        :rtype: List of :class:`geoserver.LayerGroup`
        :raise: :class:`IOError` if any error occurs while requesting the REST API.
        """
        layergroups = self._get('layergroups')['layerGroups']['layerGroup']
        return list(map(self._layergroup_from_json, layergroups))

    def get_layergroup(self, name):
        """
        Get a specific layer group.

        :param name: Name of the layer group to get.
        :type name: string
        :return: The required layer group or None if the layer group does not exist.
        :rtype: :class:`geoserver.LayerGroup`
        :raise: :class:`IOError` if any error occurs while requesting the REST API.
        """
        if not name:
            return None
        try:
            layer = self._get('layergroups/' + name)['layerGroup']
            return self._layergroup_from_json(layer)
        except IOError as e:
            logging.info(e)
            return None

    def get_styles(self):
        """
        Get all the styles in the GeoServer instance.

        :return: All the styles.
        :rtype: List of :class:`geoserver.Style`
        :raise: :class:`IOError` if any error occurs while requesting the REST API.
        """
        styles = self._get('styles')['styles']['style']
        return list(map(lambda s: Style(s['name'], self), styles))

    def get_style(self, name):
        """
        Get a specific style.

        :param name: Name of the style to get.
        :type name: string
        :return: The required style or None if the style does not exist.
        :rtype: :class:`geoserver.Style`
        :raise: :class:`IOError` if any error occurs while requesting the REST API.
        """
        try:
            style = self._get('styles/' + name)['style']
            return Style(style['name'], self)
        except IOError as e:
            logging.info(e)
            return None

    def reset(self):
        """
        Resets all store, raster, and schema caches.

        :rtype: None
        :raise: :class:`IOError` if any error occurs while requesting the REST API.
        """
        self._request('reset', method='POST')

    def reload(self):
        """
        Reloads the GeoServer catalog and configuration from disk.

        :rtype: None
        :raise: :class:`IOError` if any error occurs while requesting the REST API.
        """
        self._request('reload', method='POST')

    def fonts(self):
        """
        Get all the available fonts in the GeoServer instance

        :return: All the fonts.
        :rtype: Array of string
        :raise: :class:`IOError` if any error occurs while requesting the REST API.
        """
        return self._get('fonts')['fonts']

    def create_workspace(self, name, namespace):
        """
        Creates a new workspace.

        :param name: Name of the workspace to create.
        :param namespace: Namespace of the workspace to create.
        :type name: string
        :type namespace: string
        :rtype: None
        :raise: :class:`ValueError` if the name or the namespace are invalid.
        :raise: :class:`IOError` if any error occurs while requesting the REST API.
        """
        if not name:
            raise ValueError('Invalid name')
        if not namespace:
            raise ValueError('Invalid namespace')

        ws = json.dumps({
            'workspace': {
                'name': name
            }
        })
        ns = json.dumps({
            'namespace': {
                'prefix': name,
                'uri': namespace
            }
        })
        self._request(
            'workspaces', method='POST', expected_code=201,
            headers={'Content-type': 'application/json'}, data=ws)
        self._request(
            'namespaces/' + name, method='PUT',
            headers={'Content-type': 'application/json'}, data=ns)

    def create_style(self, name, sld):
        """
        Creates a new style.

        :param name: Name of the style to create.
        :param sld: SLD content of the style.
        :type name: string
        :type sld: string
        :rtype: None
        :raise: :class:`ValueError` if the name is invalid.
        :raise: :class:`IOError` if any error occurs while requesting the REST API.
        """
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
                'styles/' + name, method='PUT', extension='', data=sld,
                headers={'Content-type': 'application/vnd.ogc.sld+xml'})
        except OSError as e:
            try:
                self._request('styles/' + name, method='DELETE')
            except OSError as e:
                logging.error(e)
            raise IOError('Cannot add style', e)

    def _get(self, path):
        return self._request(path)

    def _request(self, path, #pylint: disable=too-many-arguments
                 extension='.json',
                 method='get',
                 expected_code=200,
                 headers=None,
                 data=None):
        url = urljoin(self.url, path)
        if format and not url.endswith(extension):
            url = url + extension
        f = getattr(requests, method.lower())
        r = f(url, auth=(self.user, self.password), data=data, headers=headers) #pylint: disable=not-callable
        if r.status_code != expected_code:
            msg = ("Cannot perform {} request to {}. Response code is {}"
                   .format(method, url, r.status_code))
            raise IOError(msg)
        if format == '.json':
            try:
                return r.json() if r.text else None
            except ValueError:
                return r.text
        else:
            return r.text
