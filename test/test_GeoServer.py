import unittest
from geoserver.GeoServer import GeoServer


class GeoServerTestCase(unittest.TestCase):
    def test_get_workspaces(self):
        pass

    def test_get_workspace_existing(self):
        pass

    def test_get_workspace_non_existing(self):
        pass

    def test_get_datastores_no_workspace(self):
        pass

    def test_get_datastores_specific_workspace(self):
        pass

    def test_get_datastore_existing(self):
        pass

    def test_get_datastore_non_existing(self):
        pass

    def test_get_layers(self):
        pass

    def test_get_layer_existing(self):
        pass

    def test_get_layer_non_existing(self):
        pass

    def test_get_layergroups(self):
        pass

    def test_get_layergroup_existing(self):
        pass

    def test_get_layergroup_non_existing(self):
        pass

    def test_get_style(self):
        pass

    def test_get_style_existing(self):
        pass

    def test_get_style_non_existing(self):
        pass

    def test_create_workspace(self):
        pass

    def test_create_workspace_invalid_name(self):
        pass

    def test_create_workspace_invalid_namespace(self):
        pass

    def test_create_style(self):
        pass

    def test_create_style_invalid_name(self):
        pass

    def test_create_style_invalid_sld(self):
        pass

    def test_reset(self):
        pass

    def test_reload(self):
        pass

    def test_fonts(self):
        pass


if __name__ == '__main__':
    unittest.main()
