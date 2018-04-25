import unittest
import requests
from geoserver.GeoServer import GeoServer
from geoserver.Workspace import Workspace
from geoserver.Style import Style
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

    def test_get_workspace_None(self):
        self.assertTrue(self.gs.get_workspace(None) is None)

    def test_get_datastores_no_workspace(self):
        try:
            self.gs.get_datastores(None)
            assert False
        except ValueError:
            pass

    def test_get_datastores(self):
        ds = self.gs.get_datastores('tiger')
        ws = self.gs.get_workspace('tiger')
        self.assertEqual(ds, ws.get_datastores())

    def test_get_datastore_no_workspace(self):
        try:
            self.gs.get_datastore('ds', None)
            assert False
        except ValueError:
            pass

    def test_get_datastore(self):
        ds = self.gs.get_datastore('tiger_roads', 'tiger')
        ws = self.gs.get_workspace('tiger')
        self.assertEqual(ds, ws.get_datastore('tiger_roads'))

    def test_get_layers(self):
        layers = self.gs.get_layers()
        names = set(map(lambda layer: layer.get_name(), layers))
        expected = set(['sf:sfdem', 'nurc:Img_Sample', 'tiger:tiger_roads',
                        'sf:restricted', 'topp:tasmania_cities',
                        'tiger:giant_polygon',
                        'topp:tasmania_state_boundaries',
                        'sf:archsites', 'tiger:poi', 'nurc:Arc_Sample',
                        'topp:states', 'tiger:poly_landmarks',
                        'topp:tasmania_water_bodies', 'sf:bugsites',
                        'nurc:Pk50095', 'topp:tasmania_roads', 'sf:roads',
                        'nurc:mosaic', 'sf:streams'])
        self.assertEqual(names, expected)

    def test_get_layer_existing(self):
        layer = self.gs.get_layer('tiger:tiger_roads')
        self.assertEqual('tiger:tiger_roads', layer.get_name())
        self.assertEqual('tiger_roads', layer.get_default_style().get_name())
        self.assertEqual(self.gs, layer.get_geoserver())

    def test_get_layer_non_existing(self):
        self.assertTrue(self.gs.get_layer('invalid') is None)

    def test_get_layer_None(self):
        self.assertTrue(self.gs.get_layer(None) is None)

    def test_get_layergroups(self):
        layergroups = self.gs.get_layergroups()
        names = set(map(lambda group: group.get_name(), layergroups))
        expected = set(['spearfish', 'tasmania', 'tiger-ny'])
        self.assertEqual(names, expected)

    def test_get_layergroup_existing(self):
        group = self.gs.get_layergroup('spearfish')
        self.assertEqual('spearfish', group.get_name())
        names = set(map(lambda layer: layer.get_name(), group.get_layers()))
        expected = set(['sf:sfdem', 'sf:streams', 'sf:roads', 'sf:restricted',
                        'sf:archsites', 'sf:bugsites'])
        self.assertEqual(names, expected)

    def test_get_layergroup_non_existing(self):
        self.assertTrue(self.gs.get_layergroup('invalid') is None)

    def test_get_layergroup_None(self):
        self.assertTrue(self.gs.get_layergroup(None) is None)

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
        style = self.gs.get_style('burg')
        self.assertEqual(type(style), Style)
        self.assertEqual('burg', style.get_name())

    def test_get_style_non_existing(self):
        self.assertTrue(self.gs.get_style('invalid') is None)

    def test_create_workspace(self):
        pass

    def test_create_workspace_invalid_name(self):
        pass

    def test_create_workspace_invalid_namespace(self):
        pass

    def test_create_style(self):
        with open('test/sample.sld') as f:
            sld = f.read()
        self.gs.create_style('new_style', sld)
        self.gs.get_style('new_style').delete()

    def test_create_style_invalid_name(self):
        with open('test/sample.sld') as f:
            sld = f.read()
        try:
            self.gs.create_style('', sld)
            assert False
        except ValueError:
            pass

    def test_create_style_None_name(self):
        with open('test/sample.sld') as f:
            sld = f.read()
        try:
            self.gs.create_style(None, sld)
            assert False
        except ValueError:
            pass

    def test_create_style_invalid_sld(self):
        with open('test/invalid.sld') as f:
            sld = f.read()
        try:
            self.gs.create_style('new_style', sld)
            assert False
        except IOError:
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
