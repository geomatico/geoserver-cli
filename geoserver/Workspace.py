from geoserver.Resource import Resource


class Workspace(Resource):
    def __init__(self, name, geoserver, namespace):
        Resource.__init__(self, name, geoserver)
        pass

    def delete(self):
        pass

    def get_datastores(self):
        pass

    def get_datastore(self, name):
        pass

    def get_namespace(self):
        pass

    def set_namespace(self):
        pass

    def create_datastore(self, name, type, opts):
        pass
