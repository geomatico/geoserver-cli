#!/usr/bin/env python
# # -*- coding: utf-8 -*-
HELP = "Show GeoServer's fonts"


def configure_parser(parser):
    parser.description = HELP


def run(_, geoserver):
    print('\n'.join(geoserver.fonts()))
