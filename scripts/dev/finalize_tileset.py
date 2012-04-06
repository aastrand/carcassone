#!/usr/bin/env python

import sys
import logging
import random
import time
import copy
import json
import simplejson

from carcassonne.engine.util import validate_tileset_config
from carcassonne.engine.util import load_config
from carcassonne.engine.board import Board, PlayedTile
from carcassonne.engine.tile import ROTATIONS, EDGES, MATERIALS
from carcassonne.render.render import HtmlRenderer

def get_connections(material, startnum):
    if material == 'road':
        return [str(a) for a in xrange(startnum, startnum +3)]
    elif material == 'city':
        return [str(startnum)]
    elif material == 'field':
        return [str(startnum)]
    else:
        print 'wtf? %s' % (material)
        raise Exception()

def main():
    if len(sys.argv) < 2:
        sys.stderr.write("Usage: transform_tileset <tileset>\n")
        return 1

    logging.getLogger().setLevel(logging.DEBUG)

    f = open(sys.argv[1]).read()
    j = simplejson.loads(f)

    tiles = {}
    for name, tile in j['tiles'].items():
        complete = True
        for cname, c in tile['positions'].items():
            if 'connection' in c and c['connection'] == '?':
                complete = False
                break

        if complete:
            tiles[tile['name']] = tile['positions']

    for name, tile in j['tiles'].items():
        tile['positions'] = tiles[tile['name']]

    print json.dumps(j, sort_keys=True, indent=4)

if __name__ == '__main__':
    sys.exit(main())