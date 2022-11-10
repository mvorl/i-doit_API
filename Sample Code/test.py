#!/usr/bin/env python3

import os
import sys
import configparser
import pathlib
import pprint

from idoitapi import *


mypath = pathlib.Path(os.path.realpath(__file__))
outputfile = mypath.with_suffix('.output')
print('Output can be found in {}'.format(outputfile))
fh = open(outputfile, 'w')
pp = pprint.PrettyPrinter(stream=fh)

sys.argv.append('demo')  # Make sure sys.argv[1] is defined
config_path = mypath.parent / ('.config.' + sys.argv[1])

cp = configparser.ConfigParser(interpolation=None)
cp.read(config_path)
config = cp[cp.default_section]

api = API(
    url=config['IDOIT_URL'],
    key=config['IDOIT_API_KEY'],
    username=config['IDOIT_USERNAME'],
    password=config['IDOIT_PASSWORD'],
    language=config.get('IDOIT_LANGUAGE', 'en'),
)

try:
    api.login()
except Exception as exc:
    print('Exception while logging in: ', exc)
    exit(1)

print('Get info about object types')
response = CMDBObjectTypes(api).read()
fh.write("\nCMDBObjectTypes:\n")
pp.pprint(response)

print('Get info about categories')
response = CMDBCategoryInfo(api).read_all()
fh.write("\nCMDBCategoryInfo:\n")
pp.pprint(response)

print('Get info about objects')
response = CMDBObjects(api).read()
fh.write("\nCMDBObjects:\n")
pp.pprint(response)

object_id = response[0]['id']

print('Get all info about a particular object')
response = CMDBObject(api).load(object_id)
fh.write("\nCMDBObject({}):\n".format(object_id))
pp.pprint(response)

api.logout()
fh.close()
