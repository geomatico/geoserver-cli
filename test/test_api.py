import unittest
from geoserver import api


class GeoServerAPITestCase(unittest.TestCase):
    """Tests for `geoserver/api.py`."""

    def test_api_method(self):
        """ Testing method """
        self.assertEqual(api.test(5), 10)


if __name__ == '__main__':
    unittest.main()
