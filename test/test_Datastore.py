# pylint: disable=too-many-public-methods,missing-docstring

import unittest
from test.utils import GEOSERVER_URL
from geoserver.GeoServer import GeoServer
from geoserver.Datastore import TYPE_POSTGIS, TYPE_SHP, TYPE_GEOTIFF


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
        except TypeError:
            ds.delete()

    def test_set_file_shp(self):
        ds = self.gs.get_datastore('nyc', 'tiger')
        self.assertEqual('file:data/nyc', ds.get_file())

        ds.set_file('new_file')
        self.assertEqual('file:new_file', ds.get_file())

        ds.set_file('data/nyc')
        self.assertEqual('file:data/nyc', ds.get_file())
        ds = self.gs.get_datastore('nyc', 'tiger')
        self.assertEqual('file:data/nyc', ds.get_file())

    def test_set_file_shp_invalid(self):
        ds = self.gs.get_datastore('nyc', 'tiger')
        try:
            ds.set_file(None)
            assert False
        except ValueError:
            pass

    def test_set_file_geotiff(self):
        ds = self.gs.get_datastore('sfdem', 'sf')
        self.assertEqual('file:data/sf/sfdem.tif', ds.get_file())

        ds.set_file('new_file')
        self.assertEqual('file:new_file', ds.get_file())

        ds.set_file('data/sf/sfdem.tif')
        self.assertEqual('file:data/sf/sfdem.tif', ds.get_file())
        ds = self.gs.get_datastore('sfdem', 'sf')
        self.assertEqual('file:data/sf/sfdem.tif', ds.get_file())

    def test_set_file_geotiff_invalid(self):
        ds = self.gs.get_datastore('sfdem', 'sf')
        try:
            ds.set_file(None)
            assert False
        except ValueError:
            pass

    def test_set_file_postgis(self):
        ds = self._create_postgis_datastore()
        try:
            ds.set_file(None)
            assert False
        except TypeError:
            ds.delete()

    def test_create_layer_vector(self):
        ds = self.gs.get_datastore('states_shapefile', 'topp')
        self.assertEqual(1, len(ds.get_layers()))
        ds.get_layer('states').delete()
        self.assertEqual(0, len(ds.get_layers()))
        ds.create_layer('states')
        layers = ds.get_layers()
        self.assertEqual(1, len(layers))
        self.assertEqual('topp:states', layers[0].get_name())


    def test_create_layer_raster(self):
        ds = self.gs.get_datastore('sfdem', 'sf')
        self.assertEqual(1, len(ds.get_layers()))
        ds.get_layer('sfdem').delete()
        self.assertEqual(0, len(ds.get_layers()))
        ds.create_layer('sfdem')
        layers = ds.get_layers()
        self.assertEqual(1, len(layers))
        self.assertEqual('sf:sfdem', layers[0].get_name())

    def test_create_layer_existing(self):
        ds = self.gs.get_datastore('states_shapefile', 'topp')
        try:
            ds.create_layer('states')
        except IOError:
            pass

    def test_create_layer_invalid(self):
        ds = self.gs.get_datastore('states_shapefile', 'topp')
        try:
            ds.create_layer('invalid')
        except IOError:
            pass

    def test_get_file_postgis(self):
        ds = self._create_postgis_datastore()
        try:
            ds.get_file()
            assert False
        except TypeError:
            ds.delete()

    def test_get_file_shp(self):
        ds = self.gs.get_datastore('nyc', 'tiger')
        self.assertEqual('file:data/nyc', ds.get_file())

    def test_get_file_geotiff(self):
        ds = self.gs.get_datastore('sfdem', 'sf')
        self.assertEqual('file:data/sf/sfdem.tif', ds.get_file())

    def test_get_type_postgis(self):
        ds = self._create_postgis_datastore()
        self.assertEqual(TYPE_POSTGIS, ds.get_type())
        ds.delete()

    def test_get_type_shp(self):
        ds = self.gs.get_datastore('nyc', 'tiger')
        self.assertEqual(TYPE_SHP, ds.get_type())

    def test_get_type_geotiff(self):
        ds = self.gs.get_datastore('sfdem', 'sf')
        self.assertEqual(TYPE_GEOTIFF, ds.get_type())

    def test_get_database_params_shp(self):
        try:
            self.gs.get_datastore('nyc', 'tiger').get_database_params()
            assert False
        except TypeError:
            pass

    def test_get_database_params_geotiff(self):
        try:
            self.gs.get_datastore('sfdem', 'sf').get_database_params()
            assert False
        except TypeError:
            pass


if __name__ == '__main__':
    unittest.main()
