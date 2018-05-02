# pylint: disable=W0212
"""
Datastore
"""
from geoserver.Resource import Resource


TYPE_POSTGIS = 'postgis'
TYPE_SHP = 'shp'
TYPE_GEOTIFF = 'geotiff'


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
        path = 'workspaces/' + self.workspace.get_name() + '/'
        if self.datastore_type == TYPE_SHP or self.datastore_type == TYPE_POSTGIS:
            path = path + 'datastores/' + self.name
        else:
            path = path + 'coveragestores/' + self.name
        self.geoserver._request(path, method='DELETE')

    def get_layers(self):
        pass

    def get_layer(self, name):
        pass

    def get_layergroups(self):
        pass

    def get_layergroup(self, name):
        pass

    def set_database_params(self, params):
        pass

    def set_file(self, file):
        pass

    def create_layer(self, name):
        pass

    def create_layergroup(self, name, layers):
        pass

    def get_type(self):
        return self.datastore_type

    def get_file(self):
        return self.file

    def get_database_params(self):
        return self.db_params

    def __eq__(self, other):
        return (self.__class__ == other.__class__ and
                self.name == other.name and
                self.geoserver == other.geoserver)
