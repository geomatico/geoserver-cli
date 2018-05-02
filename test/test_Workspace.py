# pylint: disable=too-many-public-methods,missing-docstring

import unittest
from test.AbstractGeoServerTestCase import AbstractGeoServerTestCase
from geoserver.Datastore import TYPE_SHP, TYPE_POSTGIS, TYPE_GEOTIFF


class WorkspaceTestCase(AbstractGeoServerTestCase):
    def test_get_geoserver(self):
        ws = self.gs.get_workspace('cite')
        self.assertEqual(self.gs, ws.get_geoserver())

    def test_get_datastores(self):
        # Datastores
        ws = self.gs.get_workspace('tiger')
        datastores = ws.get_datastores()
        self.assertEqual(1, len(datastores))
        self.assertEqual('nyc', datastores[0].get_name())

        # Coverage stores
        ws = self.gs.get_workspace('nurc')
        datastores = ws.get_datastores()
        self.assertEqual(4, len(datastores))
        names = set(map(lambda ds: ds.get_name(), datastores))
        expected = set(['arcGridSample', 'img_sample2', 'mosaic',
                        'worldImageSample'])
        self.assertEqual(names, expected)

    def test_get_datastore_existing(self):
        ws = self.gs.get_workspace('tiger')
        ds = ws.get_datastore('nyc')
        self.assertEqual(self.gs, ds.get_geoserver())
        self.assertEqual(ws, ds.get_workspace())
        self.assertEqual('nyc', ds.get_name())
        self.assertEqual(TYPE_SHP, ds.get_type())
        self.assertEqual('file:data/nyc', ds.get_file())

        ws = self.gs.get_workspace('nurc')
        ds = ws.get_datastore('mosaic')
        self.assertEqual(self.gs, ds.get_geoserver())
        self.assertEqual(ws, ds.get_workspace())
        self.assertEqual('mosaic', ds.get_name())
        self.assertEqual(TYPE_GEOTIFF, ds.get_type())
        self.assertEqual(
            'file:coverages/mosaic_sample/mosaic.shp', ds.get_file())

    def test_get_datastore_qualified_name(self):
        ws = self.gs.get_workspace('tiger')
        ds = ws.get_datastore('tiger:nyc')
        self.assertEqual(self.gs, ds.get_geoserver())
        self.assertEqual(ws, ds.get_workspace())
        self.assertEqual('nyc', ds.get_name())
        self.assertEqual(TYPE_SHP, ds.get_type())
        self.assertEqual('file:data/nyc', ds.get_file())

    def test_get_datastore_non_existing(self):
        ws = self.gs.get_workspace('tiger')
        self.assertTrue(ws.get_datastore('invalid') is None)

    def test_get_namespace(self):
        ws = self.gs.get_workspace('tiger')
        self.assertEqual('http://www.census.gov', ws.get_namespace())

    def test_set_namespace(self):
        original = 'http://www.census.gov'
        ws = self.gs.get_workspace('tiger')
        self.assertEqual(original, ws.get_namespace())
        ws.set_namespace('another')
        ws = self.gs.get_workspace('tiger')
        self.assertEqual('another', ws.get_namespace())
        ws.set_namespace(original)
        self.assertEqual(original, ws.get_namespace())

    def test_set_namespace_invalid(self):
        try:
            self.gs.get_workspace('tiger').set_namespace(None)
            assert False
        except ValueError:
            pass

    def test_create_datastore_postgis(self):
        ws = self.gs.get_workspace('tiger')
        ws.create_datastore('new_postgis', TYPE_POSTGIS,
                            self.DEFAULT_DB_OPTS)

        ds = ws.get_datastore('new_postgis')
        self.assertEqual('new_postgis', ds.get_name())
        self.assertEqual(TYPE_POSTGIS, ds.get_type())
        del self.DEFAULT_DB_OPTS['password']
        self.assertEqual(self.DEFAULT_DB_OPTS, ds.get_database_params())

    def test_create_datastore_postgis_invalid_schema(self):
        ws = self.gs.get_workspace('tiger')
        self.DEFAULT_DB_OPTS['schema'] = None
        try:
            ws.create_datastore('new_postgis', TYPE_POSTGIS,
                                self.DEFAULT_DB_OPTS)
            assert False
        except ValueError:
            pass

    def test_create_datastore_postgis_invalid_user(self):
        ws = self.gs.get_workspace('tiger')
        self.DEFAULT_DB_OPTS['user'] = None
        try:
            ws.create_datastore('new_postgis', TYPE_POSTGIS,
                                self.DEFAULT_DB_OPTS)
            assert False
        except ValueError:
            pass

    def test_create_datastore_postgis_invalid_pass(self):
        ws = self.gs.get_workspace('tiger')
        self.DEFAULT_DB_OPTS['password'] = None
        try:
            ws.create_datastore('new_postgis', TYPE_POSTGIS,
                                self.DEFAULT_DB_OPTS)
            assert False
        except ValueError:
            pass

    def test_create_datastore_postgis_invalid_host(self):
        ws = self.gs.get_workspace('tiger')
        self.DEFAULT_DB_OPTS['host'] = None
        try:
            ws.create_datastore('new_postgis', TYPE_POSTGIS,
                                self.DEFAULT_DB_OPTS)
            assert False
        except ValueError:
            pass

    def test_create_datastore_postgis_invalid_port(self):
        ws = self.gs.get_workspace('tiger')
        self.DEFAULT_DB_OPTS['port'] = None
        try:
            ws.create_datastore('new_postgis', TYPE_POSTGIS,
                                self.DEFAULT_DB_OPTS)
            assert False
        except ValueError:
            pass

    def test_create_datastore_postgis_invalid_database(self):
        ws = self.gs.get_workspace('tiger')
        self.DEFAULT_DB_OPTS['database'] = None
        try:
            ws.create_datastore('new_postgis', TYPE_POSTGIS,
                                self.DEFAULT_DB_OPTS)
            assert False
        except ValueError:
            pass

    def test_create_datastore_shp(self):
        ws = self.gs.get_workspace('tiger')
        ws.create_datastore('new_shp', TYPE_SHP, 'data/myfile.shp')

        ds = ws.get_datastore('new_shp')
        self.assertEqual('new_shp', ds.get_name())
        self.assertEqual(TYPE_SHP, ds.get_type())
        self.assertEqual('file:data/myfile.shp', ds.get_file())

    def test_create_datastore_shp_invalid_file(self):
        try:
            ws = self.gs.get_workspace('tiger')
            ws.create_datastore('new_shp', TYPE_SHP, None)
            assert False
        except ValueError:
            pass

    def test_create_datastore_geotiff(self):
        ws = self.gs.get_workspace('nurc')
        ws.create_datastore('new_geotiff', TYPE_GEOTIFF, 'data/myfile.tiff')

        ds = ws.get_datastore('new_geotiff')
        self.assertEqual('new_geotiff', ds.get_name())
        self.assertEqual(TYPE_GEOTIFF, ds.get_type())
        self.assertEqual('file:data/myfile.tiff', ds.get_file())

    def test_create_datastore_geotiff_invalid_file(self):
        try:
            ws = self.gs.get_workspace('nurc')
            ws.create_datastore('new_geotiff', TYPE_GEOTIFF, None)
            assert False
        except ValueError:
            pass

    def test_create_datastore_invalid_type(self):
        try:
            ws = self.gs.get_workspace('tiger')
            ws.create_datastore('new_shp', 'invalid_type', 'data/myfile.shp')
            assert False
        except ValueError:
            pass

    def test_create_datastore_invalid_name(self):
        try:
            ws = self.gs.get_workspace('tiger')
            ws.create_datastore(None, TYPE_SHP, 'data/myfile.shp')
            assert False
        except ValueError:
            pass


if __name__ == '__main__':
    unittest.main()
