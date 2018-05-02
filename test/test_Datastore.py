# pylint: disable=too-many-public-methods,missing-docstring

import unittest
from test.utils import GEOSERVER_URL
from geoserver.GeoServer import GeoServer


class LayerTestCase(unittest.TestCase):
    def setUp(self):
        self.gs = GeoServer(GEOSERVER_URL, 'admin', 'geoserver')

    def test_get_geoserver(self):
        ds = self.gs.get_datastore('nyc', 'tiger')
        self.assertEqual(self.gs, ds.get_geoserver())

    def test_delete(self):
        pass

    def test_get_workspace(self):
        ds = self.gs.get_datastore('nyc', 'tiger')
        self.assertEqual(ds.get_workspace(), self.gs.get_workspace('tiger'))

    def test_get_layers(self):
        ds = self.gs.get_datastore('nyc', 'tiger')
        layers = ds.get_layers()
        names = set(map(lambda ds: ds.get_name(), layers))
        expected = set(['tiger:giant_polygon',
                        'tiger:poi',
                        'tiger:poly_landmarks',
                        'tiger:tiger_roads'])
        self.assertEqual(names, expected)

    def test_get_layer_existing(self):
        ds = self.gs.get_datastore('nyc', 'tiger')
        layer = ds.get_layer('tiger_roads')
        self.assertEqual('tiger:tiger_roads', layer.get_name())
        self.assertEqual('tiger_roads', layer.get_default_style().get_name())

    def test_get_layer_non_existing(self):
        ds = self.gs.get_datastore('nyc', 'tiger')
        self.assertTrue(ds.get_layer('invalid') is None)

    def test_get_layer_from_another_datastore(self):
        ds = self.gs.get_datastore('nyc', 'tiger')
        self.assertTrue(ds.get_layer('topp:states') is None)

    def test_get_layergroups(self):
        pass

    def test_get_layergroup_existing(self):
        pass

    def test_get_layergroup_non_existing(self):
        pass

    def test_set_database_params_all(self):
        pass

    def test_set_database_params_some(self):
        pass

    def test_set_database_params_invalid(self):
        pass

    def test_set_database_params_not_postgis(self):
        pass

    def test_set_file_shp(self):
        pass

    def test_set_file_shp_invalid(self):
        pass

    def test_set_file_geotiff(self):
        pass

    def test_set_file_geotiff_invalid(self):
        pass

    def test_set_file_not_shp_or_geotiff(self):
        pass

    def test_create_layer(self):
        pass

    def test_create_layer_invalid(self):
        pass

    def test_create_layergroup(self):
        pass

    def test_create_layergroup_invalid(self):
        pass


if __name__ == '__main__':
    unittest.main()
