#!/usr/bin/env python
# # -*- coding: utf-8 -*-

HELP = 'Reload GeoServer'


def configure_parser(parser):
    parser.description = HELP


def run(_, geoserver):
    geoserver.reload()
    print('GeoServer reload success.')
