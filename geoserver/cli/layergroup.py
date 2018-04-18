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
        title='Commands', dest='layer_cmd',
        help='Get info from all layer groups')

    # Get
    get = subparsers.add_parser(
        GET,
        help='Gets info from a specific layer group',
        description='Gets info from a specific layer group')
    get.add_argument('name', help='Name of the layer group')

    # Create
    create = subparsers.add_parser(CREATE, help='Creates a new layer',
                                   description='Creates a new layer')
    create.add_argument('name', help='Name of the layer group to create')
    create.add_argument(
        '-w', '--workspace',
        help='Name of the workspace containing the layer group',
        required=False)
    create.add_argument(
        '-d', '--datastore',
        help='Name of the datastore containing the layer group',
        required=True)
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


def run(args):
    print(args)
