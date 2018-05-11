from geoserver.Resource import Resource


class Layer(Resource):
    def __init__(self, name, geoserver, default_style, datastore, workspace):
        Resource.__init__(self, name, geoserver)
        self.default_style = default_style

    def delete(self):
        pass

    def set_default_style(self, style):
        self.default_style = style

    def get_default_style(self):
        return self.default_style
