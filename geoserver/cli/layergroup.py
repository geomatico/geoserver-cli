#!/usr/bin/env python
# # -*- coding: utf-8 -*-

import argparse

HELP = 'Manage layer groups'
GET = 'get'
CREATE = 'create'
UPDATE = 'update'
DELETE = 'delete'


def configure_parser(parser):
    parser.description = HELP
    subparsers = parser.add_subparsers(
        title='Commands', dest='layergroup_cmd',
        help='Get info from all layer groups')

    # Get
    get = subparsers.add_parser(
        GET,
        help='Gets info from a specific layer group',
        description='Gets info from a specific layer group')
    get.add_argument('name', help='Name of the layer group')

    # Create
    create = subparsers.add_parser(CREATE, help='Creates a new layer group',
                                   description='Creates a new layer group')
    create.add_argument('name', help='Name of the layer group to create')
    create.add_argument('layers', nargs=argparse.REMAINDER,
                        help='Layers to add to the group')

    # Update
    update = subparsers.add_parser(UPDATE, help='Updates a layer group',
                                   description='Updates a layer group')
    update.add_argument('name', help='Name of the layer')
    update.add_argument(
        'layers', nargs=argparse.REMAINDER,
        help=('Layers to add/remove to/from the group. '
              'Note that you don\'t need to specify all the layers. '
              'If the layer already exists in the group, it will be removed; '
              'if not it will be added.'))

    # Delete
    delete = subparsers.add_parser(DELETE, help='Deletes a layer group',
                                   description='Deletes a layer group')
    delete.add_argument('name', help='Name of the layer group')


def run(args, geoserver):
    if not args.layergroup_cmd:
        groups = geoserver.get_layergroups()
        groups = map(lambda g: g.get_name(), groups)
        print('\n'.join(groups))
    elif args.layergroup_cmd == GET:
        group = geoserver.get_layergroup(args.name)
        if group:
            layers = group.get_layers()
            datastores = map(lambda l: '  ' + l.get_name(), layers)

            print(group.get_name())
            print('\nLayers:')
            print('\n'.join(datastores))
        else:
            print('The layer group does not exist.')
    elif args.layergroup_cmd == CREATE:
        geoserver.create_layergroup(args.name, args.layers)
        print('Layer group created successfully.')
    elif args.layergroup_cmd == UPDATE:
        group = geoserver.get_layergroup(args.name)
        if group:
            group.set_layers(args.layers)
            print('Layer group updated successfully.')
        else:
            print('The layer group does not exist.')
    elif args.layergroup_cmd == DELETE:
        group = geoserver.get_layergroup(args.name)
        if group:
            group.delete()
            print('Layer group deleted successfully.')
        else:
            print('The layer group does not exist.')
