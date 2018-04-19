"""
GeoServer
"""


class GeoServer:
    def __init__(self):
        pass

    def get_workspaces(self):
        """
        Gets all workspaces.
        """
        pass

    def get_workspace(self, name):
        """
        Gets a workspace by name.

        :param name: Description of parameter `name`.
        :type name: string
        """
        pass

    def get_datastores(self, workspace=None):
        pass

    def get_datastore(self, name, workspace=None):
        pass

    def get_layers(self):
        pass

    def get_layer(self, name):
        pass

    def get_layergroups(self):
        pass

    def get_layergroup(self, name):
        pass

    def get_styles(self):
        pass

    def get_style(self, name):
        pass

    def reset(self):
        pass

    def reload(self):
        pass

    def fonts(self):
        pass

    def create_workspace(self, name, namespace):
        pass

    def create_style(self, name, sld):
        pass
