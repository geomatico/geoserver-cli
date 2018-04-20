from geoserver.Resource import Resource


class Layer(Resource):
    def __init__(self, name, geoserver, description, datastore, workspace):
        Resource.__init__(self, name, geoserver)
        pass

    def get_workspace(self):
        pass

    def get_datastore(self):
        pass

    def delete(self):
        pass

    def set_style(self, style):
        pass

    def get_style(self):
        pass

    def set_description(self, description):
        pass

    def get_description(self):
        pass
