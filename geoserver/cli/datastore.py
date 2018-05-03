#!/usr/bin/env python
# # -*- coding: utf-8 -*-
from geoserver.Datastore import TYPE_SHP, TYPE_GEOTIFF, TYPE_POSTGIS


HELP = 'Manage datastores'
GET = 'get'
CREATE = 'create'
UPDATE = 'update'
DELETE = 'delete'
POSTGIS = 'pg'
GEOTIFF = 'tiff'
SHP = 'shp'


def configure_parser(parser):
    parser.description = HELP
    parser.add_argument('-w', '--workspace',
                        help='Workspace containing the datastore',
                        required=True)
    subparsers = parser.add_subparsers(
        title='Commands', dest='store_cmd',
        help='Get info from all datastores')

    # Get
    get = subparsers.add_parser(
        GET,
        help='Gets info from a specific datastore',
        description='Gets info from a specific datastore')
    get.add_argument('name', help='Name of the datastore')

    # Create
    create = subparsers.add_parser(CREATE, help='Create a new datastore',
                                   description='Create a new datastore')
    create_subparsers = create.add_subparsers(
        title='Types', dest='datastore_type',
        help='Datastore type')

    # Create PostGIS
    create_postgis = create_subparsers.add_parser(
        POSTGIS,
        help='Create a new PostGIS datastore',
        description='Create a new PostGIS datastore')
    create_postgis.add_argument(
        '-e',
        help=('Use PG_* variables for connecting to the '
              'database instead of command parameters'),
        action='store_true')
    create_postgis.add_argument('name', help='Name of the datastore')
    create_postgis.add_argument(
        '-H', '--host', help='Database host', required=True)
    create_postgis.add_argument(
        '-p', '--port', help='Database port', required=True)
    create_postgis.add_argument(
        '-d', '--database', help='Database name', required=True)
    create_postgis.add_argument(
        '-s', '--schema', help='Database schema', required=True)
    create_postgis.add_argument(
        '-u', '--user', help='Database user', required=True)
    create_postgis.add_argument(
        '-P', '--password', help='Database password', required=True)

    # Create SHP
    create_shp = create_subparsers.add_parser(
        SHP,
        help='Create a new SHP datastore',
        description='Create a new SHP datastore')
    create_shp.add_argument('name', help='Name of the datastore')
    create_shp.add_argument('-f', '--file', help='Shapefile', required=True)

    # Create GeoTIFF
    create_tiff = create_subparsers.add_parser(
        GEOTIFF,
        help='Create a new GeoTIFF datastore',
        description='Create a new GeoTIFF datastore')
    create_tiff.add_argument('name', help='Name of the datastore')
    create_tiff.add_argument('-f', '--file', help='GeoTIFF', required=True)

    # Update
    update = subparsers.add_parser(UPDATE, help='Update a datastore',
                                   description='Update a datastore')
    update_subparsers = update.add_subparsers(
        title='Types', dest='datastore_type',
        help='Datastore type')

    # Update PostGIS
    update_postgis = update_subparsers.add_parser(
        POSTGIS,
        help='Update a PostGIS datastore',
        description='Update a PostGIS datastore')
    update_postgis.add_argument(
        '-e',
        help=('Use PG_* variables for connecting to the '
              'database instead of command parameters'),
        action='store_true')
    update_postgis.add_argument('name', help='Name of the datastore')
    update_postgis.add_argument('-H', '--host', help='Database host')
    update_postgis.add_argument('-p', '--port', help='Database port')
    update_postgis.add_argument('-d', '--database', help='Database name')
    update_postgis.add_argument('-s', '--schema', help='Database schema',)
    update_postgis.add_argument('-u', '--user', help='Database user')
    update_postgis.add_argument('-P', '--password', help='Database password')

    # Delete
    delete = subparsers.add_parser(DELETE, help='Deletes a datastore',
                                   description='Deletes a datastore')
    delete.add_argument('name', help='Name of the datastore')


def run(args, geoserver):
    ws = geoserver.get_workspace(args.workspace)
    if not args.store_cmd:
        ds = ws.get_datastores()
        ds = map(lambda d: d.get_name(), ds)
        print('\n'.join(ds))
    elif args.store_cmd == GET:
        ds = ws.get_datastore(args.name)
        if ds:
            layers = ds.get_layers()
            layers = map(lambda l: '  ' + l.get_name(), layers)
            print(ds.get_name())
            print('\nLayers:')
            print('\n'.join(layers))
        else:
            print('The datastore does not exist.')
    elif args.store_cmd == CREATE:
        if args.datastore_type == 'shp':
            dtype = TYPE_SHP
            opts = args.file
        elif args.datastore_type == 'tiff':
            dtype = TYPE_GEOTIFF
            opts = args.file
        else:
            dtype = TYPE_POSTGIS
            opts = {
                'host': args.host,
                'port': args.port,
                'user': args.user,
                'password': args.password,
                'database': args.database,
                'schema': args.schema
            }
        ws.create_datastore(args.name, dtype, opts)
        print('Datastore created successfully.')
    elif args.store_cmd == UPDATE:
        if args.datastore_type != 'pg':
            return
        datastore = ws.get_datastore(args.name)
        if datastore:
            datastore.set_database_params(vars(args))
            print('Datastore updated successfully.')
        else:
            print('The datastore does not exist.')
    elif args.store_cmd == DELETE:
        datastore = ws.get_datastore(args.name)
        if datastore:
            datastore.delete()
            print('Datastore deleted successfully.')
        else:
            print('The datastore does not exist.')
