from geoserver.Resource import Resource


TYPE_POSTGIS = 'postgis'
TYPE_SHP = 'shp'
TYPE_GEOTIFF = 'geotiff'


class Datastore(Resource):
    def __init__(self, name, geoserver, workspace, type, opts):
        Resource.__init__(self, name, geoserver)
        pass

    def get_workspace(self):
        pass

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

    def __eq__(self, other):
        return (self.__class__ == other.__class__ and
            self.name == other.name and
            self.geoserver == other.geoserver)
