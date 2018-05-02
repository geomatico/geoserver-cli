# pylint: disable=W0212,C0301
"""
Datastore
"""
import json
from geoserver.Resource import Resource


TYPE_POSTGIS = 'postgis'
TYPE_SHP = 'shp'
TYPE_GEOTIFF = 'geotiff'


def _get_dict_from_db_params(name, opts):
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
                    '@key': 'schema',
                    '$': opts['schema']
                }, {
                    '@key': 'dbtype',
                    '$': 'postgis'
                }]
            }
        }
    }
    if 'password' in opts:
        data['dataStore']['connectionParameters']['entry'].append({
            '@key': 'passwd',
            '$': opts['password']
        })
    return data


class Datastore(Resource):
    """
    An object representing a GeoServer store (including datastores, coveragestores, etc.).

    :param name: The name of the workspace
    :param geoserver: The :class:`geoserver.GeoServer` instance this workspace belongs to.
    :param workspace: The workspace containing this datastore.
    :param datastore_type: The type of the datastore to create. Use TYPE_* constants.
    :param opts: The options to create the datastore.
        They vary depending on the datastore type:

        * For `TYPE_SHP`: A string with the file path.
        * For `TYPE_GEOTIFF`: A string with the file path.
        * For `TYPE_POSTGIS`: A dict containing `host`, `port`, `database`, `schema`, `user`, `password`.
    :type name: string
    :type geoserver: :class:`geoserver.GeoServer`
    :type workspace: :class:`geoserver.Workspace`
    :type datastore_type: string
    """

    def __init__(self, name, geoserver, workspace, datastore_type, opts):  # pylint: disable=too-many-arguments
        Resource.__init__(self, name, geoserver)
        self.workspace = workspace
        self.datastore_type = datastore_type
        if (datastore_type == TYPE_SHP or datastore_type == TYPE_GEOTIFF):
            self.file = opts
        elif datastore_type == TYPE_POSTGIS:
            self.db_params = opts
        else:
            raise ValueError('Unrecognized datastore type: ' + datastore_type)

    def get_workspace(self):
        """
        Gets the workspace this datastore belongs to.

        :return: The workspace containing this datastore.
        :rtype: :class:`geoserver.Workspace`
        """
        return self.workspace

    def delete(self):
        """
        Deletes the datastore from GeoServer.

        :rtype: None
        :raise: :class:`IOError` if any error occurs while requesting the REST API.
        """
        path = 'workspaces/' + self.workspace.get_name() + '/'
        if self.datastore_type == TYPE_SHP or self.datastore_type == TYPE_POSTGIS:
            path = path + 'datastores/' + self.name
        else:
            path = path + 'coveragestores/' + self.name
        self.geoserver._request(path, method='DELETE')

    def get_layers(self):
        """
        Get all the layers in this datastore.

        :return: All the layers in this datastore.
        :rtype: List of :class:`geoserver.Layer`
        :raise: :class:`IOError` if any error occurs while requesting the REST API.
        """
        layers = self.geoserver.get_layers()
        return list(filter(lambda l: l.get_datastore() == self, layers))

    def get_layer(self, name):
        """
        Get a specific layer from this datastore.

        :param name: Name of the layer to get.
        :type name: string
        :return: The required layer or None if the layer does not exist in this datastore (even if it exists in GeoServer).
        :rtype: :class:`geoserver.Layer`
        :raise: :class:`IOError` if any error occurs while requesting the REST API.
        """
        layer = self.geoserver.get_layer(name)
        return layer if layer is not None and layer.get_datastore() == self else None

    def get_layergroups(self):
        pass

    def get_layergroup(self, name):
        pass

    def set_database_params(self, params):
        """
        Sets the database params for a PostGIS datastore.

        :param opts: A dictionary containing some of these keys `host`, `port`, `database`, `schema`, `user`, `password`. Other keys are ignored.
        :type opts: Dictionary
        :rtype: None
        :raise: :class:`TypeError` if the datastore type is not PostGIS.
        :raise: :class:`IOError` if any error occurs while requesting the REST API.
        """
        if self.datastore_type != TYPE_POSTGIS:
            raise TypeError(
                'Cannot set database params for type: ' + self.datastore_type)
        valid_keys = ('host', 'port', 'database', 'schema', 'user', 'password')
        valid_params = {k: params[k] for k in valid_keys if k in params}
        new_params = self.db_params.copy()
        new_params.update(valid_params)
        data = _get_dict_from_db_params(self.name, new_params)
        path = 'workspaces/' + self.workspace.get_name() + '/datastores/' + self.name
        self.geoserver._request(
            path, method='PUT',
            headers={'Content-type': 'application/json'}, data=json.dumps(data))
        self.db_params = new_params

    def set_file(self, file):
        pass

    def create_layer(self, name):
        pass

    def create_layergroup(self, name, layers):
        pass

    def get_type(self):
        """
        Get the type of this datastore. Use TYPE_* constants.

        :return: The type of this datastore.
        :rtype: string
        """
        return self.datastore_type

    def get_file(self):
        """
        Get the file for this datastore.

        :return: The URL of the file for this datastore (only if it is not a PostGIS datastore).
        :rtype: string
        :raise: :class:`TypeError` if the datastore type is PostGIS.
        """
        if self.datastore_type != TYPE_POSTGIS:
            return self.file
        else:
            raise TypeError(
                'Cannot get file for type: ' + self.datastore_type)

    def get_database_params(self):
        """
        Get the database parameters for this datastore.

        :return: A dictionary containing the database parameters for this datastore (only if it is a PostGIS datastore).
        :rtype: Dictionary
        :raise: :class:`TypeError` if the datastore type is not PostGIS.
        """
        if self.datastore_type == TYPE_POSTGIS:
            return self.db_params
        else:
            raise TypeError(
                'Cannot get database params for type: ' + self.datastore_type)

    def __eq__(self, other):
        return (self.__class__ == other.__class__ and
                self.name == other.name and
                self.workspace == other.workspace and
                self.geoserver == other.geoserver)
