#!/usr/bin/env python
# # -*- coding: utf-8 -*-

HELP = 'Manage styles'
GET = 'get'
CREATE = 'create'
UPDATE = 'update'
DELETE = 'delete'


def configure_parser(parser):
    parser.description = HELP
    subparsers = parser.add_subparsers(
        title='Commands', dest='style_cmd',
        help='Get info from all styles')

    # Get
    get = subparsers.add_parser(
        GET,
        help='Gets info from a specific style',
        description='Gets info from a specific style')
    get.add_argument('name', help='Name of the style')

    # Create
    create = subparsers.add_parser(CREATE, help='Creates a new style',
                                   description='Creates a new style')
    create.add_argument('name', help='Name of the style to create')
    create.add_argument('-f', '--file',
                        help='SLD file containing the style to create',
                        required=True)

    # Update
    update = subparsers.add_parser(UPDATE, help='Updates a style',
                                   description='Updates a style')
    update.add_argument('name', help='Name of the style')
    update.add_argument('-f', '--file',
                        help='SLD file containing the style to update',
                        required=True)

    # Delete
    delete = subparsers.add_parser(DELETE, help='Deletes a style',
                                   description='Deletes a style')
    delete.add_argument('name', help='Name of the style')


def run(args):
    print(args)
