from geoserver.Resource import Resource


class Layer(Resource):
    def __init__(self, name, geoserver, default_style, datastore, workspace):
        Resource.__init__(self, name, geoserver)
        pass

    def get_workspace(self):
        pass

    def get_datastore(self):
        pass

    def delete(self):
        pass

    def set_default_style(self, style):
        pass

    def get_default_style(self):
        pass
