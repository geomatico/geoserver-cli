#!/usr/bin/env python
# # -*- coding: utf-8 -*-

HELP = 'Reset GeoServer'


def configure_parser(parser):
    parser.description = HELP


def run(args):
    print(args)
