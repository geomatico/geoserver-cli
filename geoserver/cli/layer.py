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
                        required=True)
    create.add_argument('-d', '--datastore',
                        help='Name of the datastore containing the layer',
                        required=True)
    create.add_argument('name', help='Name of the layer to create')

    # Update
    update = subparsers.add_parser(UPDATE, help='Updates a layer',
                                   description='Updates a layer')
    update.add_argument('name', help='Name of the layer')
    update.add_argument('-s', '--style',
                        help='Name of the default style to use for the layer',
                        required=True)

    # Delete
    delete = subparsers.add_parser(DELETE, help='Deletes a layer',
                                   description='Deletes a layer')
    delete.add_argument('name', help='Name of the layer')


def run(args, geoserver):
    if not args.layer_cmd:
        layers = geoserver.get_layers()
        layers = map(lambda l: l.get_name(), layers)
        print('\n'.join(layers))
    elif args.layer_cmd == GET:
        layer = geoserver.get_layer(args.name)
        if layer:
            style = layer.get_default_style()
            print(layer.get_name())
            print('Default style: ' + style.get_name())
        else:
            print('The layer does not exist.')
    elif args.layer_cmd == CREATE:
        ws = geoserver.get_workspace(args.workspace)
        if not ws:
            print('Workspace does not exist.')
            return
        ds = ws.get_datastore(args.datastore)
        if not ds:
            print('Datastore does not exist.')
            return
        ds.create_layer(args.name)
        print('Layer created successfully.')
    elif args.layer_cmd == UPDATE:
        layer = geoserver.get_layer(args.name)
        if layer:
            layer.set_default_style(args.style)
            print('Layer updated successfully.')
        else:
            print('The layer does not exist.')
    elif args.layer_cmd == DELETE:
        layer = geoserver.get_layer(args.name)
        if layer:
            layer.delete()
            print('Layer deleted successfully.')
        else:
            print('The layer does not exist.')
