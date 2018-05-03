# pylint: disable=too-many-public-methods,missing-docstring,I1101

import unittest
from test.AbstractGeoServerTestCase import AbstractGeoServerTestCase
import xml.etree.ElementTree as ET


def _get_style_name(style):
    elem = ET.fromstring(style.get_sld())
    xpath = './/{http://www.opengis.net/sld}UserStyle/{http://www.opengis.net/sld}Name'
    return elem.find(xpath).text


class StyleTestCase(AbstractGeoServerTestCase):
    def test_set_sld(self):
        with open('test/burg.sld') as f:
            burg = f.read()
        with open('test/capitals.sld') as f:
            capitals = f.read()

        style = self.gs.get_style('burg')
        self.assertEqual('burg', _get_style_name(style))
        style.set_sld(capitals)
        self.assertEqual('capitals', _get_style_name(style))
        style.set_sld(burg)

    def test_set_sld_invalid(self):
        style = self.gs.get_style('burg')
        try:
            with open('test/invalid.sld') as f:
                style.set_sld(f.read())
                assert False
        except IOError:
            pass


if __name__ == '__main__':
    unittest.main()
