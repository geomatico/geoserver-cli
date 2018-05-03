# pylint: disable=too-many-public-methods,missing-docstring

import unittest
from test.AbstractGeoServerTestCase import AbstractGeoServerTestCase


class LayerTestCase(AbstractGeoServerTestCase):
    def test_get_workspace(self):
        layer = self.gs.get_layer('topp:states')
        self.assertEqual(self.gs.get_workspace('topp'), layer.get_workspace())

    def test_get_datastore(self):
        layer = self.gs.get_layer('topp:states')
        ws = self.gs.get_workspace('topp')
        ds = ws.get_datastore('states_shapefile')
        self.assertEqual(ds, layer.get_datastore())

    def test_get_default_style(self):
        layer = self.gs.get_layer('topp:states')
        style = layer.get_default_style()
        self.assertEqual(style, self.gs.get_style('polygon'))

    def test_set_default_style_by_name(self):
        layer = self.gs.get_layer('topp:states')
        self.assertEqual(layer.get_default_style(), self.gs.get_style('polygon'))
        layer.set_default_style('burg')
        self.assertEqual(layer.get_default_style(), self.gs.get_style('burg'))
        layer.set_default_style('polygon')
        self.assertEqual(layer.get_default_style(), self.gs.get_style('polygon'))

    def test_set_default_style_by_instance(self):
        layer = self.gs.get_layer('topp:states')
        self.assertEqual(layer.get_default_style(), self.gs.get_style('polygon'))
        layer.set_default_style(self.gs.get_style('burg'))
        self.assertEqual(layer.get_default_style(), self.gs.get_style('burg'))
        layer.set_default_style(self.gs.get_style('polygon'))
        self.assertEqual(layer.get_default_style(), self.gs.get_style('polygon'))

    def test_set_default_style_invalid(self):
        layer = self.gs.get_layer('topp:states')
        try:
            layer.set_default_style('invalid')
            assert False
        except ValueError:
            pass


if __name__ == '__main__':
    unittest.main()
