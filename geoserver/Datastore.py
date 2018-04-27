from geoserver.Resource import Resource


TYPE_POSTGIS = 'postgis'
TYPE_SHP = 'shp'
TYPE_GEOTIFF = 'geotiff'


class Datastore(Resource):
    def __init__(self, name, geoserver, workspace, datastore_type, opts):  # pylint: disable=too-many-arguments
        Resource.__init__(self, name, geoserver)
        self.workspace = workspace
        self.datastore_type = datastore_type
        if (datastore_type == TYPE_SHP or datastore_type == TYPE_GEOTIFF):
            self.file = opts
        elif datastore_type == TYPE_POSTGIS:
            self.db_params = opts

    def get_workspace(self):
        return self.workspace

    def delete(self):
        pass

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
