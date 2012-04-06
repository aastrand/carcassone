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
    for name, tile in conf['tiles'].items():
        new_conf['tiles'][name] = copy.deepcopy(conf['tiles'][name])
        del new_conf['tiles'][name]['positions']
        new_conf['tiles'][name]['positions'] = {}
        #print "analyzing %s"  % (name)
        type_to_con = {}
        con_to_type = {}
        for what, data in tile['edges'].items():
            type = data['type']
            c = data['connections']
            if len(c) == 3:
                type_to_con.setdefault(type, set()).add(c[1])
                con_to_type[c[1]] = type
                type_to_con.setdefault('field', set()).add(c[0])
                type_to_con.setdefault('field', set()).add(c[2])
                con_to_type[c[0]] = 'field'
                con_to_type[c[2]] = 'field'
                
            else:
                type_to_con.setdefault(type, set()).add(c[0])
                con_to_type[c[0]] = type
        #print type_to_con
        #print con_to_type

        analyzed_connections = {}
        for c in tile['connections']:
            cset = set()
            for i in c:
                cset.add(i)
            if type_to_con[con_to_type[c[0]]] == cset:
                #print "connection is of type %s" % con_to_type[c[0]]
                analyzed_connections[con_to_type[c[0]]] = c[0]
            #else:
                #print "connection is ambigious"

        for pos, role in conf['tiles'][name]['positions'].items():
            new_conf['tiles'][name]['positions'][pos] = {}
            new_conf['tiles'][name]['positions'][pos]['role'] = role
            if role_to_type[role] in analyzed_connections:
                new_conf['tiles'][name]['positions'][pos]['connection'] = analyzed_connections[role_to_type[role]]
            else:
                new_conf['tiles'][name]['positions'][pos]['connection'] = '?'
            #new_conf['tiles'][name]['positions'][pos]['connection'] = role


    print json.dumps(new_conf, sort_keys=True, indent=4)

    #filename = 'board.html'
    #print "Rendering to %s" % (filename)
    #html = HtmlRenderer.render(b)
    #file = open(filename, 'w')
    #file.write(html)
    #file.close()

if __name__ == '__main__':
    sys.exit(main())