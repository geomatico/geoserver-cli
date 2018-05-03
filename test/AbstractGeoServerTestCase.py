# pylint: disable=missing-docstring

import unittest
from geoserver.GeoServer import GeoServer


class AbstractGeoServerTestCase(unittest.TestCase):
    def setUp(self):
        self.gs = GeoServer("http://localhost:8080/geoserver",
                            'admin', 'geoserver')
        self.DEFAULT_DB_OPTS = {
            'host': 'localhost',
            'port': '5432',
            'user': 'docker',
            'password': 'docker',
            'database': 'gis',
            'schema': 'public'
        }