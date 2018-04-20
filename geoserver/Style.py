from geoserver.Resource import Resource


class Style(Resource):
    def __init__(self, name, geoserver):
        Resource.__init__(self, name, geoserver)

    def delete(self):
        pass

    def set_sld(self, sld):
        pass
