#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import sys

import prymatex

usage="pmx.py [options] [files]"

description = prymatex.__doc__

version = prymatex.get_version(),

epilog = """This program comes with ABSOLUTELY NO WARRANTY.
This is free software, and you are welcome to redistribute
it under certain conditions; for details see LICENSE.txt.
Check project page at %s""" % prymatex.__url__

try:
    import argparse
except ImportError: # Python < 2.7
    from prymatex.utils import argparse

parser = argparse.ArgumentParser(usage=usage, 
    description = description,
    version = version,
    epilog = epilog)

parser.add_argument('file', metavar='file', type=unicode,
    nargs='*', help='A file/s to edit', default=[])
parser.add_argument('-f', '--files', metavar='file', type=unicode,
    nargs='+', help='A file/s to edit', default=[])

# Reverts custom options
parser.add_argument('--reset-settings', metavar='reste_settings', default = False, 
                    help = 'Restore default settings for selected profile')

parser.add_argument('-p', '--profile', metavar='profile', nargs="?", default="",
                help = "Change profile")

# Maybe useful for some debugging information
parser.add_argument('-d','--devel', default=False, action='store_true',
                help = 'Enable developer mode. Useful for plugin developers.')

parser.add_argument('--verbose', default=0, type=int,
                help = 'Set verbose level from 0 to 4.')

parser.add_argument('--log-pattern', default='', type=str,
                help = 'Set filter pattern for logging')

def parse():
    filenames = None
    projects_path = None
    extra_plugins = None
    try:
        
        opts = parser.parse_args()

        filenames = opts.file \
            if isinstance(opts.file, list) \
            else [opts.file]
        filenames += opts.files \
            if hasattr(opts, 'files') \
            else []
    except Exception, reason:
        print("Arguments couldn't be parsed.")
        print(reason)
    return opts, filenames
