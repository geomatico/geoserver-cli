import unittest
from geoserver.Workspace import Workspace
from test.utils import *


class WorkspaceTestCase(unittest.TestCase):
    def test_get_geoserver(self):
        pass

    def test_delete(self):
        pass

    def test_get_datastores(self):
        pass

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
