import unittest
import requests
from geoserver.GeoServer import GeoServer
from geoserver.Workspace import Workspace
from test.utils import *


class GeoServerTestCase(unittest.TestCase):
    def setUp(self):
        self.gs = GeoServer(GEOSERVER_URL, 'admin', 'geoserver')

    def test_get_workspaces(self):
        workspaces = self.gs.get_workspaces()
        names = set(map(lambda ws: ws.get_name(), workspaces))
        expected = set(['cite', 'tiger', 'nurc',
                        'sde', 'it.geosolutions', 'topp', 'sf'])
        self.assertEqual(names, expected)

    def test_get_workspace_existing(self):
        ws = self.gs.get_workspace('tiger')
        self.assertEqual(type(ws), Workspace)
        self.assertEqual('tiger', ws.get_name())
        self.assertEqual('http://www.census.gov', ws.get_namespace())
        self.assertEqual(self.gs, ws.get_geoserver())

    def test_get_workspace_non_existing(self):
        self.assertTrue(self.gs.get_workspace('invalid') is None)

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

    def test_get_styles(self):
        styles = self.gs.get_styles()
        names = set(map(lambda style: style.get_name(), styles))
        expected = set(['burg', 'capitals', 'cite_lakes', 'dem', 'generic',
                        'giant_polygon', 'grass', 'green', 'line', 'poi',
                        'point', 'poly_landmarks', 'polygon', 'pophatch',
                        'population', 'rain', 'raster', 'restricted',
                        'simple_roads', 'simple_streams', 'tiger_roads'])
        self.assertEqual(names, expected)

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
        # Just make sure it doesn't break
        self.gs.reset()

    def test_reload(self):
        # Just make sure it doesn't break
        self.gs.reload()

    def test_fonts(self):
        fonts = self.gs.fonts()
        self.assertTrue('Arial' in fonts)
        self.assertTrue('Times New Roman' in fonts)
        self.assertTrue('Verdana' in fonts)


if __name__ == '__main__':
    unittest.main()
