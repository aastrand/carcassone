#!/usr/bin/env python

import sys
import logging
import random

from carcassonne.engine.util import validate_tileset_config
from carcassonne.engine.util import load_config
from carcassonne.engine.board import Board
from carcassonne.engine.tile import ROTATIONS
from carcassonne.render.render import HtmlRenderer

def main():
    if len(sys.argv) < 2:
        sys.stderr.write("Usage: construct_random_board <tileset>\n")
        return 1

    logging.getLogger().setLevel(logging.INFO)

    print "Loading ..."
    json = load_config(sys.argv[1])

    validate_tileset_config(json, set(['thief', 'knight', 'monk', 'farmer']),
                            set(['city', 'field', 'road']))


    print "Constructing ..."
    b = Board(json)
    failed_count = 0
    while len(b.tilesleft) > 0:
        tile = random.sample(b.tilesleft, 1)[0]
        locations = b.playable_locations(tile)
        location = random.sample(locations, 1)[0]

        for r in ROTATIONS.values():
            if b.is_legal_on_location(tile, location, ROTATIONS[r]):
                b.add_to_board(tile, location, ROTATIONS[r])
                break
        else:
            failed_count += 1

    print 'Done, had to retry %d tiles' % failed_count

    print b
    d = b.dimensions()
    print 'Board size: %dx%d' % (d[0], d[1])

    filename = 'board.html'
    print "Rendering to %s" % (filename)
    html = HtmlRenderer.render(b)
    file = open(filename, 'w')
    file.write(html)
    file.close()

if __name__ == '__main__':
    sys.exit(main())