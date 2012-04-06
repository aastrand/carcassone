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
from carcassonne.render.render import Renderer

role_to_type = {'thief': 'road',
                'monk': 'cloister',
                'knight': 'city',
                'farmer': 'field'}

def main():
    if len(sys.argv) < 2:
        sys.stderr.write("Usage: transform_tileset <tileset>\n")
        return 1

    logging.getLogger().setLevel(logging.DEBUG)

    conf = load_config(sys.argv[1])

    validate_tileset_config(conf, set(['city', 'field', 'road']))


    new_conf = {}
    new_conf['tiles'] = {}
    new_conf['base_tiles'] = {}
    for name, tile in conf['tiles'].items():
        new_conf['base_tiles'][tile['name']] = copy.deepcopy(tile)
        del new_conf['base_tiles'][tile['name']]['name']
        new_conf['tiles'][name] = tile['name'] 

    for name, tile in new_conf['base_tiles'].items():
        positions = []
        for pos, data in tile['positions'].items():
            #print pos, data
            if 'connection' in data:
                #print pos
                x, y = Renderer.pos_to_tile_xy(pos, 0)
                #print x, y
                xp = int(float(x)/float(Renderer.tile_width) * 100.0)
                yp = int(float(y)/float(Renderer.tile_height) * 100.0)
                #print xp, yp
                this_pos = {}
                this_pos['connection'] = data['connection']
                this_pos['x'] = xp
                this_pos['y'] = yp
                positions.append(this_pos)
        del tile['positions']
        tile['positions'] = positions

    print json.dumps(new_conf, sort_keys=True, indent=4)

    #filename = 'board.html'
    #print "Rendering to %s" % (filename)
    #html = HtmlRenderer.render(b)
    #file = open(filename, 'w')
    #file.write(html)
    #file.close()

if __name__ == '__main__':
    sys.exit(main())