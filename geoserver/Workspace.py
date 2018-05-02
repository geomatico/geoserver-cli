# pylint: disable=W0212
"""
Workspace
"""
import json
from geoserver.Resource import Resource
from geoserver.Datastore import Datastore, TYPE_SHP, TYPE_POSTGIS, TYPE_GEOTIFF


def _get_value_from_params(datastore, param_name):
    params = datastore['connectionParameters']['entry']
    value = next(filter(lambda p: p['@key'] == param_name, params), None)
    return value['$'] if value else None


def _check_dict_value(opts, *keys):
    for key in keys:
        if not opts[key]:
            raise ValueError('Invalid ' + key + ': ' + (opts[key] or ''))


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

    def _get_datastore_from_json(self, datastore, is_vector):
        name = datastore['name']
        url = _get_value_from_params(
            datastore, 'url') if is_vector else datastore['url']
        if url:
            datastore_type = TYPE_SHP if is_vector else TYPE_GEOTIFF
            return Datastore(name, self.geoserver, self, datastore_type, url)
        elif datastore['type'] == 'PostGIS':
            opts = {
                'host': _get_value_from_params(datastore, 'host'),
                'port': _get_value_from_params(datastore, 'port'),
                'database': _get_value_from_params(datastore, 'database'),
                'schema': _get_value_from_params(datastore, 'schema'),
                'user': _get_value_from_params(datastore, 'user')
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

    def _get_json_or_none(self, path):
        try:
            return self.geoserver._request(path)
        except IOError:
            return None

    def get_datastore(self, name):
        """
        Get a specific datastore from this workspace.

        :param name: Name of the datastore to get.
        :type name: string
        :return: The required datastore or None if the datastore does not exist.
        :rtype: :class:`geoserver.Datastore`
        :raise: :class:`ValueError` if the name is invalid (contains, more than one colon symbol, the qualified name belongs to a different workspace, etc.)
        :raise: :class:`IOError` if any error occurs while requesting the REST API.
        """
        if ':' in name:
            parts = name.split(':')
            if len(parts) > 2 or self.name != parts[0]:
                raise ValueError('Invalid name: ' + name)
            name = parts[1]
        path = 'workspaces/' + self.name + '/datastores/' + name
        ds = self._get_json_or_none(path)
        if ds:
            return self._get_datastore_from_json(ds['dataStore'], True)

        path = 'workspaces/' + self.name + '/coveragestores/' + name
        ds = self._get_json_or_none(path)
        return self._get_datastore_from_json(ds['coverageStore'], False) if ds else None

    def get_namespace(self):
        """
        Gets the namespace of the workspace.

        :return: The namespace.
        :rtype: string.
        """
        return self.namespace

    def set_namespace(self, namespace):
        """
        Sets the namespace of the workspace.

        :param namespace: The namespace to set.
        :type namespace: string.
        :rtype: None
        :raise: :class:`IOError` if any error occurs while requesting the REST API.
        :raise: :class:`ValueError` if the namespace is not valid.
        """
        if not namespace:
            raise ValueError('Invalid namespace')
        ns = json.dumps({
            'namespace': {
                'prefix': self.name,
                'uri': namespace
            }
        })
        self.geoserver._request(
            'namespaces/' + self.name, method='PUT',
            headers={'Content-type': 'application/json'}, data=ns)
        self.namespace = namespace

    def create_datastore(self, name, datastore_type, opts):
        """
        Create a new datastore in this workspace.

        :param name: The name of the datastore to create.
        :param datastore_type: The type of the datastore to create.
            Use TYPE_* constants.
        :param opts: The options to create the datastore.
            They vary depending on the datastore type:

            * For `TYPE_SHP`: A string with the file path.
            * For `TYPE_GEOTIFF`: A string with the file path.
            * For `TYPE_POSTGIS`: A dict containing `host`, `port`, `database`, `schema`, `user`, `password`.
        :type name: string
        :type datastore_type: string
        :raise: :class:`IOError` if any error occurs while requesting the REST API.
        :raise: :class:`ValueError` if name, the datastore type or the options are not valid.
        :rtype: None
        """
        if not name:
            raise ValueError('Invalid name')
        path = 'workspaces/' + self.name
        data = None
        if datastore_type == TYPE_SHP:
            if not opts:
                raise ValueError('Invalid file: ' + (opts or ''))
            data = {
                'dataStore': {
                    'name': name,
                    'connectionParameters': {
                        'entry': [{
                            '@key': 'url',
                            '$': 'file:' + str(opts)
                        }]
                    }
                }
            }
            path = path + '/datastores'
        elif datastore_type == TYPE_GEOTIFF:
            if not opts:
                raise ValueError('Invalid file: ' + (opts or ''))
            data = {
                'coverageStore': {
                    'name': name,
                    'type': 'GeoTIFF',
                    'url': 'file:' + str(opts),
                    'workspace': {
                        'name': self.name,
                        'href': self.geoserver.url + 'workspaces/' + self.name
                    }
                }
            }
            path = path + '/coveragestores'
        elif datastore_type == TYPE_POSTGIS:
            _check_dict_value(opts, 'host', 'port', 'database', 'user',
                              'password', 'schema')
            data = {
                'dataStore': {
                    'name': name,
                    'connectionParameters': {
                        'entry': [{
                            '@key': 'host',
                            '$': opts['host']
                        }, {
                            '@key': 'port',
                            '$': opts['port']
                        }, {
                            '@key': 'database',
                            '$': opts['database']
                        }, {
                            '@key': 'user',
                            '$': opts['user']
                        }, {
                            '@key': 'passwd',
                            '$': opts['password']
                        }, {
                            '@key': 'schema',
                            '$': opts['schema']
                        }, {
                            '@key': 'passwd',
                            '$': opts['password']
                        }, {
                            '@key': 'dbtype',
                            '$': 'postgis'
                        }]
                    }
                }
            }
            path = path + '/datastores'

        if not data:
            raise ValueError('Unrecognized datastore type: ' + datastore_type)

        self.geoserver._request(
            path, method='POST', expected_code=201,
            headers={'Content-type': 'application/json'}, data=json.dumps(data))

    def __eq__(self, other):
        return (self.__class__ == other.__class__ and
                self.name == other.name and
                self.namespace == other.namespace and
                self.geoserver == other.geoserver)
