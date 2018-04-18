#!/usr/bin/env python
# # -*- coding: utf-8 -*-

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
    create_postgis.add_argument('-c', '--url', help='Database URL')
    create_postgis.add_argument('-u', '--user', help='Database user')
    create_postgis.add_argument('-p', '--pass', help='Database password')
    create_postgis.add_argument('-s', '--schema',
                                help='Database schema',
                                required=True)
    create_postgis.add_argument('-w', '--workspace',
                                help='Workspace containing the datastore')

    # Create SHP
    create_shp = create_subparsers.add_parser(
        SHP,
        help='Create a new SHP datastore',
        description='Create a new SHP datastore')
    create_shp.add_argument('name', help='Name of the datastore')
    create_shp.add_argument('-f', '--file', help='Shapefile')
    create_shp.add_argument('-w', '--workspace',
                            help='Workspace containing the datastore')

    # Create GeoTIFF
    create_tiff = create_subparsers.add_parser(
        GEOTIFF,
        help='Create a new GeoTIFF datastore',
        description='Create a new GeoTIFF datastore')
    create_tiff.add_argument('name', help='Name of the datastore')
    create_tiff.add_argument('-f', '--file', help='GeoTIFF')
    create_tiff.add_argument('-w', '--workspace',
                             help='Workspace containing the datastore')

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
    update_postgis.add_argument('-c', '--url', help='Database URL')
    update_postgis.add_argument('-u', '--user', help='Database user')
    update_postgis.add_argument('-p', '--pass', help='Database password')
    update_postgis.add_argument('-s', '--schema', help='Database schema',)

    # Delete
    delete = subparsers.add_parser(DELETE, help='Deletes a datastore',
                                   description='Deletes a datastore')
    delete.add_argument('name', help='Name of the datastore')


def run(args):
    print(args)
