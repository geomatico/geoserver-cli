from geoserver.Resource import Resource


class LayerGroup(Resource):
    def __init__(self, name, geoserver, description, datastore, workspace):
        Resource.__init__(self, name, geoserver)
        pass

    def get_workspace(self):
        pass

    def get_datastore(self):
        pass

    def delete(self):
        pass

    def set_layers(self, layers):
        pass

    def get_layers(self):
        pass
