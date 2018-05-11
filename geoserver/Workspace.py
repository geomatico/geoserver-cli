from geoserver.Resource import Resource


class Workspace(Resource):
    def __init__(self, name, geoserver, namespace):
        Resource.__init__(self, name, geoserver)
        self.namespace = namespace

    def delete(self):
        self.geoserver._request('workspaces/' + self.name, method='DELETE')

    def get_datastores(self):
        pass

    def get_datastore(self, name):
        pass

    def get_namespace(self):
        return self.namespace

    def set_namespace(self):
        pass

    def create_datastore(self, name, type, opts):
        pass
