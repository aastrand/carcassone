#!/usr/bin/env python

import sys
import logging
import random
import time
import copy
import json

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

    conf = load_config(sys.argv[1])

    validate_tileset_config(conf, set(['city', 'field', 'road']))


    
#    for tilenum, tilename in json['tiles'].items():
#        tile = json['base_tiles'][tilename]
#        if 'edges' in conf:
#            edges = {}
#            startnum = 1
#            for edge, material in conf['edges'].items():
#                edges[edge] = {}
#                edges[edge]['type'] = material
#                edges[edge]['connections'] = get_connections(material, startnum)
#                startnum += len(edges[edge]['connections'])
#            new_json['base_tiles'][tile] = {}
#            new_json['base_tiles'][tile]['edges'] = edges
#
#    print new_json

    b = Board(conf)
    new_conf = {}
    new_conf['tiles'] = {}
    for tilenum, ptile in b.boardtiles.items():
        tile = {}
        new_conf['tiles'][tilenum] = tile
        tile['name'] = ptile.tile.name
        tile['positions'] = {}
        for pos, role in ptile.tile.positions:
            tile['positions'][pos] = role
        tile['edges'] = {}
        startnum = 0
        for i, edge  in enumerate(ptile.tile.edges):
            pos = EDGES.by_ordinal(i)
            tile['edges'][pos] = {}
            tile['edges'][pos]['type'] = MATERIALS.by_ordinal(edge)
            tile['edges'][pos]['connections'] = get_connections(MATERIALS.by_ordinal(edge), startnum)
            startnum += len(tile['edges'][pos]['connections'])

    print json.dumps(new_conf, sort_keys=True, indent=4)

    #filename = 'board.html'
    #print "Rendering to %s" % (filename)
    #html = HtmlRenderer.render(b)
    #file = open(filename, 'w')
    #file.write(html)
    #file.close()

if __name__ == '__main__':
    sys.exit(main())