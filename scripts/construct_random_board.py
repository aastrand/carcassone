#!/usr/bin/env python

import sys
import logging
import random
import time

from carcassonne.engine.util import validate_tileset_config
from carcassonne.engine.util import load_config
from carcassonne.engine.board import Board, PlayedTile
from carcassonne.engine.tile import ROTATIONS
from carcassonne.render.render import HtmlRenderer

def count_neighbours(board, location):
    total = set()

    location_neighbours = board.neighbours_for(location)
    count = 0
    for n in location_neighbours:
        loc = None
        if type(n) is PlayedTile:
            total.add(n)
            loc = n.location
        else:
            loc = n

        for on in board.neighbours_for(loc):
            if type(on) is PlayedTile:
                total.add(on)

    return len(total)

def main():
    if len(sys.argv) < 2:
        sys.stderr.write("Usage: construct_random_board <tileset>\n")
        return 1

    logging.getLogger().setLevel(logging.DEBUG)

    print "Loading ..."
    json = load_config(sys.argv[1])

    validate_tileset_config(json, set(['city', 'field', 'road']))


    seed = int(time.time())
    #seed = 1333213878
    print "Constructing with seed %s ..." % (seed)

    random.seed(seed)

    b = Board(json)
    failed_count = 0
    while len(b.tilesleft) > 0:
        tile = random.sample(b.tilesleft, 1)[0]
        locations = b.playable_locations(tile)

        location = None
        playable_locations = []
        location_neighbour_count = 0
        for l in locations:
            count = count_neighbours(b, l)

            if count > location_neighbour_count:
                location_neighbour_count = count
                playable_locations = []
                playable_locations.append(l)
                location = l
            elif count == location_neighbour_count:
                playable_locations.append(l)

        #location = random.sample(locations, 1)[0]
        if not playable_locations:
            logging.debug('Could not play tile %s\n%s' % (tile, b))
            failed_count += 1
            continue

        most_playable = 0
        location = None
        for l in playable_locations:
            count = 0
            for r in ROTATIONS.values():
                if b.is_legal_on_location(tile, l, ROTATIONS[r]):
                    count += 1

            if count >= most_playable:
                most_playable = count
                location = l

        #location = random.sample(playable_locations, 1)[0]

        for r in ROTATIONS.values():
            if b.is_legal_on_location(tile, location, ROTATIONS[r]):
                b.add_to_board(tile, location, ROTATIONS[r])
                break

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