import unittest
from geoserver.api import Test


class GeoServerAPITestCase(unittest.TestCase):
    """Tests for `geoserver/api.py`."""

    def test_api_method(self):
        """ Testing method """
        self.assertEqual(Test().test(100), 200)


if __name__ == '__main__':
    unittest.main()
