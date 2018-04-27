# pylint: disable=W0212
"""
Workspace
"""
from geoserver.Resource import Resource
from geoserver.Datastore import Datastore, TYPE_SHP, TYPE_POSTGIS, TYPE_GEOTIFF


def _get_value_from_params(datastore, param_name):
    params = datastore['connectionParameters']['entry']
    value = next(filter(lambda p: p['@key'] == param_name, params), None)
    return value['$'] if value else None


class Workspace(Resource):
    """
    An object representing a GeoServer workspace.

    :param name: The name of the workspace
    :param geoserver: The :class:`geoserver.GeoServer` instance this workspace belongs to.
    :param namespace: The namespace of the workspace.
    :type name: string
    :type geoserver: :class:`geoserver.GeoServer`
    :type namespace: string
    """

    def __init__(self, name, geoserver, namespace):
        Resource.__init__(self, name, geoserver)
        self.namespace = namespace

    def delete(self):
        """
        Deletes the workspace from GeoServer.

        :rtype: None
        :raise: :class:`IOError` if any error occurs while requesting the REST API.
        """
        self.geoserver._request('workspaces/' + self.name, method='DELETE')

    def _get_datastore_from_json(self, json, is_vector):
        name = json['name']
        url = _get_value_from_params(
            json, 'url') if is_vector else json['url']
        if url:
            datastore_type = TYPE_SHP if is_vector else TYPE_GEOTIFF
            return Datastore(name, self.geoserver, self, datastore_type, url)
        elif json['type'] == 'PostGIS':
            opts = {
                'host': _get_value_from_params(json, 'host'),
                'port': _get_value_from_params(json, 'port'),
                'database': _get_value_from_params(json, 'database'),
                'schema': _get_value_from_params(json, 'schema'),
                'user': _get_value_from_params(json, 'user')
            }
            return Datastore(name, self.geoserver, self, TYPE_POSTGIS, opts)

        return None

    def get_datastores(self):
        """
        Get all the datastores in this workspace.

        :return: All the datastores.
        :rtype: List of :class:`geoserver.Datastore`.
        :raise: :class:`IOError` if any error occurs while requesting the REST API.
        """
        request = self.geoserver._request
        ws = request('workspaces/' + self.name)['workspace']
        ds = request(ws['dataStores'])['dataStores']
        if ds:
            ds = ds['dataStore']
            ds = map(lambda d: request(d['href'])['dataStore'], ds)
            ds = map(lambda d: self._get_datastore_from_json(d, True), ds)

        cs = request(ws['coverageStores'])['coverageStores']
        if cs:
            cs = cs['coverageStore']
            cs = map(lambda d: request(d['href'])['coverageStore'], cs)
            cs = map(lambda d: self._get_datastore_from_json(d, False), cs)

        return (list(ds) or []) + (list(cs) or [])

    def get_datastore(self, name):
        pass

    def get_namespace(self):
        return self.namespace

    def set_namespace(self):
        pass

    def create_datastore(self, name, datastore_type, opts):
        pass

    def __eq__(self, other):
        return (self.__class__ == other.__class__ and
                self.name == other.name and
                self.namespace == other.namespace and
                self.geoserver == other.geoserver)
