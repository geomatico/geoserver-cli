class Resource:
    def __init__(self, name, geoserver):
        self.name = name
        self.geoserver = geoserver

    def get_name(self):
        return self.name

    def get_geoserver(self):
        return self.geoserver
