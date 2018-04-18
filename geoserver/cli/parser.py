#!/usr/bin/env python
# # -*- coding: utf-8 -*-

import argparse
from geoserver.cli import imports, workspace, layer, style, reload, reset, fonts

actions = {
    'import': imports,
    'ws': workspace,
    # 'ds': datastore,
    'layer': layer,
    # 'layergroup': layergroup,
    'style': style,
    'reload': reload,
    'reset': reset,
    'fonts': fonts
}

parser = argparse.ArgumentParser(description='GeoServer CLI')

subparsers = parser.add_subparsers(title='Commands', dest='cmd')

for key in sorted(actions.keys()):
    subparser = subparsers.add_parser(key, help=actions[key].HELP)
    actions[key].configure_parser(subparser)
