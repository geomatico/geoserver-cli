#!/usr/bin/env python
# # -*- coding: utf-8 -*-

HELP = 'Imports a file or directory.'


def configure_parser(parser):
    parser.description = HELP
    parser.add_argument('file', help='File or directory')


def run(args):
    print(args)
