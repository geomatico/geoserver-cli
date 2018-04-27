#pylint: disable=too-many-public-methods,missing-docstring

import unittest
from test.utils import GEOSERVER_URL
from geoserver.GeoServer import GeoServer


class WorkspaceTestCase(unittest.TestCase):
    def setUp(self):
        self.gs = GeoServer(GEOSERVER_URL, 'admin', 'geoserver')

    def test_get_geoserver(self):
        ws = self.gs.get_workspace('cite')
        self.assertEqual(self.gs, ws.get_geoserver())

    def test_delete(self):
        pass

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
        pass

    def test_get_datastore_non_existing(self):
        pass

    def test_get_namespace(self):
        pass

    def test_set_namespace(self):
        pass

    def test_set_namespace_invalid(self):
        pass

    def test_create_datastore_postgis(self):
        pass

    def test_create_datastore_postgis_invalid_schema(self):
        pass

    def test_create_datastore_postgis_invalid_user(self):
        pass

    def test_create_datastore_postgis_invalid_pass(self):
        pass

    def test_create_datastore_postgis_invalid_url(self):
        pass

    def test_create_datastore_shp(self):
        pass

    def test_create_datastore_shp_invalid_file(self):
        pass

    def test_create_datastore_geotiff(self):
        pass

    def test_create_datastore_geotiff_invalid_file(self):
        pass

    def test_create_datastore_invalid_type(self):
        pass


if __name__ == '__main__':
    unittest.main()
