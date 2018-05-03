#!/usr/bin/env python
# # -*- coding: utf-8 -*-

HELP = 'Manage workspaces'
GET = 'get'
CREATE = 'create'
UPDATE = 'update'
DELETE = 'delete'


def configure_parser(parser):
    parser.description = HELP
    subparsers = parser.add_subparsers(
        title='Commands', dest='workspace_cmd',
        help='Get info from all workspaces')

    # Get
    get = subparsers.add_parser(
        GET,
        help='Get info from a specific workspace',
        description='Get info from a specific workspace')
    get.add_argument('name', help='Name of the workspace')

    # Create
    create = subparsers.add_parser(CREATE, help='Creates a new workspace',
                                   description='Creates a new workspace')
    create.add_argument('name', help='Name of the workspace')
    create.add_argument('namespace', help='Namespace of the workspace')

    # Update
    update = subparsers.add_parser(UPDATE, help='Updates a workspace',
                                   description='Updates a workspace')
    update.add_argument('name', help='Name of the workspace')
    update.add_argument('namespace', help='Namespace of the workspace')

    # Delete
    delete = subparsers.add_parser(DELETE, help='Deletes a workspace',
                                   description='Deletes a workspace')
    delete.add_argument('name', help='Name of the workspace')


def run(args, geoserver):
    if not args.workspace_cmd:
        workspaces = geoserver.get_workspaces()
        workspaces = map(lambda w: w.get_name(), workspaces)
        print('\n'.join(workspaces))
    elif args.workspace_cmd == GET:
        ws = geoserver.get_workspace(args.name)
        if ws:
            datastores = ws.get_datastores()
            datastores = map(lambda d: '  ' + d.get_name(), datastores)

            print(ws.get_name() + ' (' + ws.get_namespace() + ')')
            print('\nDatastores:')
            print('\n'.join(datastores))
        else:
            print('The workspace does not exist.')
    elif args.workspace_cmd == CREATE:
        geoserver.create_workspace(args.name, args.namespace)
        print('Workspace created successfully.')
    elif args.workspace_cmd == UPDATE:
        ws = geoserver.get_workspace(args.name)
        if ws:
            ws.set_namespace(args.namespace)
            print('Workspace updated successfully.')
        else:
            print('The workspace does not exist.')
    elif args.workspace_cmd == DELETE:
        ws = geoserver.get_workspace(args.name)
        if ws:
            ws.delete()
            print('Workspace deleted successfully.')
        else:
            print('The workspace does not exist.')
