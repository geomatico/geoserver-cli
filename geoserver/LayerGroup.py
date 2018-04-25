from geoserver.Resource import Resource


class LayerGroup(Resource):
    def __init__(self, name, geoserver, layers):
        Resource.__init__(self, name, geoserver)
        self.layers = layers

    def delete(self):
        pass

    def set_layers(self, layers):
        pass

    def get_layers(self):
        return self.layers
