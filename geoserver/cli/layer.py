#!/usr/bin/env python
# # -*- coding: utf-8 -*-

HELP = 'Manage layers'
GET = 'get'
CREATE = 'create'
UPDATE = 'update'
DELETE = 'delete'


def configure_parser(parser):
    parser.description = HELP
    subparsers = parser.add_subparsers(
        title='Commands', dest='layer_cmd',
        help='Get info from all layers')

    # Get
    get = subparsers.add_parser(
        GET,
        help='Gets info from a specific layer',
        description='Gets info from a specific layer')
    get.add_argument('name', help='Name of the layer')

    # Create
    create = subparsers.add_parser(CREATE, help='Creates a new layer',
                                   description='Creates a new layer')
    create.add_argument('-w', '--workspace',
                        help='Name of the workspace containing the layer',
                        required=False)
    create.add_argument('-d', '--datastore',
                        help='Name of the datastore containing the layer',
                        required=True)
    create.add_argument('-s', '--style',
                        help='Name of the style to use for the layer',
                        required=False)
    create.add_argument('name', help='Name of the layer to create')

    # Update
    update = subparsers.add_parser(UPDATE, help='Updates a layer',
                                   description='Updates a layer')
    update.add_argument('name', help='Name of the layer')
    update.add_argument('-s', '--style',
                        help='Name of the style to use for the layer',
                        required=False)

    # Delete
    delete = subparsers.add_parser(DELETE, help='Deletes a layer',
                                   description='Deletes a layer')
    delete.add_argument('name', help='Name of the layer')


def run(args):
    print(args)
