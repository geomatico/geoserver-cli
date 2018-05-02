# pylint: disable=too-many-public-methods,missing-docstring

import unittest
from test.utils import GEOSERVER_URL
from geoserver.GeoServer import GeoServer
from geoserver.Datastore import TYPE_POSTGIS, TYPE_SHP


class LayerTestCase(unittest.TestCase):
    def setUp(self):
        self.gs = GeoServer(GEOSERVER_URL, 'admin', 'geoserver')
        self.DEFAULT_DB_OPTS = {
            'host': 'localhost',
            'port': '5432',
            'user': 'docker',
            'password': 'docker',
            'database': 'gis',
            'schema': 'public'
        }

    def _create_postgis_datastore(self):
        ws = self.gs.get_workspace('tiger')
        ws.create_datastore('new_postgis', TYPE_POSTGIS,
                            self.DEFAULT_DB_OPTS)
        return ws.get_datastore('new_postgis')

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

    def test_set_database_params_all(self):
        ds = self._create_postgis_datastore()
        del self.DEFAULT_DB_OPTS['password']
        self.assertEqual(self.DEFAULT_DB_OPTS, ds.get_database_params())

        new_params = {
            'host': 'another_host.com',
            'port': '65432',
            'user': 'user',
            'password': 'pass',
            'database': 'data',
            'schema': 'private'
        }
        ds.set_database_params(new_params)
        self.assertEqual(new_params, ds.get_database_params())

        ds.delete()

    def test_set_database_params_some(self):
        ds = self._create_postgis_datastore()
        del self.DEFAULT_DB_OPTS['password']
        self.assertEqual(self.DEFAULT_DB_OPTS, ds.get_database_params())

        new_params = {
            'host': 'another_host.com',
        }
        ds.set_database_params(new_params)
        db_params = ds.get_database_params()
        self.assertEqual('another_host.com', db_params['host'])
        self.assertEqual('5432', db_params['port'])
        self.assertEqual('gis', db_params['database'])
        self.assertEqual('public', db_params['schema'])
        self.assertEqual('docker', db_params['user'])

        ds.delete()

    def test_set_database_params_invalid(self):
        ds = self._create_postgis_datastore()
        del self.DEFAULT_DB_OPTS['password']
        self.assertEqual(self.DEFAULT_DB_OPTS, ds.get_database_params())

        new_params = {
            'invalid_key': 'foo',
        }
        ds.set_database_params(new_params)
        self.assertEqual(self.DEFAULT_DB_OPTS, ds.get_database_params())

        ds.delete()

    def test_set_database_params_not_postgis(self):
        ws = self.gs.get_workspace('tiger')
        ws.create_datastore('new_shp', TYPE_SHP, 'data/myfile.shp')
        ds = ws.get_datastore('new_shp')

        try:
            ds.set_database_params({'host': 'another_host.com'})
            assert False
        except ValueError:
            ds.delete()

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
