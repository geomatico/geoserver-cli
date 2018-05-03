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


def run(args, geoserver):
    if not args.style_cmd:
        styles = geoserver.get_styles()
        styles = map(lambda s: s.get_name(), styles)
        print('\n'.join(styles))
    elif args.style_cmd == GET:
        style = geoserver.get_style(args.name)
        if style:
            print(style.get_name())
            print(len(style.get_name()) * '-')
            print(style.get_sld())
        else:
            print('The style does not exist.')
    elif args.style_cmd == CREATE:
        with open(args.file) as f:
            geoserver.create_style(args.name, f.read())
            print('Style created successfully.')
    elif args.style_cmd == UPDATE:
        with open(args.file) as f:
            style = geoserver.get_style(args.name)
            if style:
                style.set_sld(f.read())
                print('Style updated successfully.')
            else:
                print('The style does not exist.')
    elif args.style_cmd == DELETE:
        style = geoserver.get_style(args.name)
        if style:
            style.delete()
            print('Style deleted successfully.')
        else:
            print('The style does not exist.')
