#!/usr/bin/env python

import sys
import simplejson
import logging

from carcassonne.engine.util import validate_tileset_config

def main():
    if len(sys.argv) < 1:
        sys.stderr.write("Usage: validate_tileset <file>\n")
        return 1

    logging.getLogger().setLevel(logging.DEBUG)

    filecontent = open(sys.argv[1]).read()
    json = simplejson.loads(filecontent)

    validate_tileset_config(json, set(['thief', 'knight', 'monk', 'farmer']),
                            set(['city', 'field', 'road']))

    sys.stdout.write('File %s is a valid tileset.\n' % (sys.argv[1]))

if __name__ == '__main__':
    sys.exit(main())