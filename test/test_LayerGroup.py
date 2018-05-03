# pylint: disable=too-many-public-methods,missing-docstring
import unittest
from test.AbstractGeoServerTestCase import AbstractGeoServerTestCase


class LayerGroupTestCase(AbstractGeoServerTestCase):
    def _check_layers(self, group, expected_names):
        layers = group.get_layers()
        names = set(map(lambda l: l.get_name(), layers))
        self.assertEqual(names, set(expected_names))

    def test_get_layers(self):
        self._check_layers(
            self.gs.get_layergroup('tasmania'),
            ['topp:tasmania_state_boundaries',
             'topp:tasmania_cities',
             'topp:tasmania_roads',
             'topp:tasmania_water_bodies'])

    def test_set_layers_add(self):
        group = self.gs.get_layergroup('tasmania')
        group.set_layers(['sf:sfdem'])

        self._check_layers(
            group,
            ['sf:sfdem',
             'topp:tasmania_state_boundaries',
             'topp:tasmania_cities',
             'topp:tasmania_roads',
             'topp:tasmania_water_bodies'])

        group.set_layers(['sf:sfdem'])

    def test_set_layers_remove(self):
        group = self.gs.get_layergroup('tasmania')
        group.set_layers(['topp:tasmania_cities'])

        self._check_layers(
            group,
            ['topp:tasmania_state_boundaries',
             'topp:tasmania_roads',
             'topp:tasmania_water_bodies'])

        group.set_layers(['topp:tasmania_cities'])

    def test_set_layers_add_and_remove(self):
        group = self.gs.get_layergroup('tasmania')
        group.set_layers(['sf:sfdem', 'topp:tasmania_cities'])

        self._check_layers(
            group,
            ['sf:sfdem',
             'topp:tasmania_state_boundaries',
             'topp:tasmania_roads',
             'topp:tasmania_water_bodies'])

        group.set_layers(['sf:sfdem', 'topp:tasmania_cities'])


if __name__ == '__main__':
    unittest.main()
