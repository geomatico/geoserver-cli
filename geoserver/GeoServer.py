"""
GeoServer
"""
import requests
import logging
from urllib.parse import urljoin
from geoserver.Workspace import Workspace


class GeoServer:
    def __init__(self, url, user, password):
        self.base_url = url + "/"
        self.url = urljoin(self.base_url, 'rest/')
        self.user = user
        self.password = password

    def _create_workspace(self, ws, namespaces=None):
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
        return list(map(lambda x: self._create_workspace(x, namespaces),
                        workspaces))

    def get_workspace(self, name):
        try:
            json = self._get('workspaces/' + name)
        except IOError as e:
            logging.info(e)
            return None

        workspace = json['workspace']
        return self._create_workspace(json['workspace'])

    def get_datastores(self, workspace=None):
        pass

    def get_datastore(self, name, workspace=None):
        pass

    def get_layers(self):
        pass

    def get_layer(self, name):
        pass

    def get_layergroups(self):
        pass

    def get_layergroup(self, name):
        pass

    def get_styles(self):
        pass

    def get_style(self, name):
        pass

    def reset(self):
        self._post('reset')

    def reload(self):
        pass

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
        url = urljoin(self.url, path, ".json")
        f = getattr(requests, method.lower())
        r = f(url, auth=(self.user, self.password), data=data)
        if r.status_code != expected_code:
            msg = ("Cannot perform {} request to {}. Response code is {}"
                   .format(method, url, r.status_code))
            raise IOError(msg)
        return r.json() if r.text else None
