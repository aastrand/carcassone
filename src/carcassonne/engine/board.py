'''
Created on Mar 11, 2012

@author: anders
'''
import logging

from carcassonne.engine.tile import Tile, EDGES, ROTATIONS

class ConfigError(ValueError):
    pass

class PlayedTile(object):
    def __init__(self, tile, neighbours, location = None, rotation = None):
        self.tile = tile
        self.neighbours = neighbours
        self.location = location
        self.rotation = rotation

        #TODO:
        self.meeple = None
        self.assigned_to = ""

    def __repr__(self):
        return "Location: %s\nRotation: %s\nNeighbours: %s\nTile: %s" % (
                self.location, self.rotation, self.neighbours, self.tile)

def compare_tileset(a, b):
    return int(a[0]) - int(b[0])

pos_to_edge = {(0, -1): EDGES.top,
               (0, 1): EDGES.bottom,
               (1, 0): EDGES.left,
               (-1, 0): EDGES.right}
def relative_pos_to_edge(location1, location2):
    x = location1[0] - location2[0]
    y = location1[1] - location2[1]
    return pos_to_edge[(x, y)]

class Board(object):
    def __init__(self, config):
        self.config = config
        self.entities = {}
        self._setup_tiles(config['base_tiles'], config['tiles'])

    def _setup_tiles(self, base_tiles, tiles):
        self.boardtiles = {}
        self.grid = {}
        self.tilesleft = set()
        self.reverse = {}
        self.edges = set()

        tileset = [(tid, tilename) for tid, tilename in tiles.items()]
        tileset = sorted(tileset, cmp=compare_tileset)

        for tid, name in tileset:
            self.boardtiles[tid] = PlayedTile(Tile(tid, name, base_tiles[name]), [])
            self.reverse.setdefault(name, []).append(self.boardtiles[tid])
            self.tilesleft.add(tid)

        self.root = self.boardtiles['1']
        self._play_tile('1', (0,0), ROTATIONS.deg0)

    def is_legal_on_location(self, tid, location, rotation):
        assert type(rotation) == int

        if tid not in self.tilesleft:
            logging.debug("Tile %s is already played" % (tid))
            return False

        if location in self.grid:
            logging.debug("Location %s, %s is already occupied" % (location))
            return False

        tile = self.boardtiles[tid]

        # Get top, bottom, left, right tiles .. if any
        neighbours = self.neighbours_for(location)

        if not any(type(n) is PlayedTile for n in neighbours):
            logging.debug("Can't play at this location, no neighbours exist: %s, %s" % (location))
            return False

        # Check if it's ok
        for n in neighbours:
            if type(n) is PlayedTile:
                edge = relative_pos_to_edge(n.location, location)
                if not n.tile.is_legal_adjecent_to(tile.tile, edge, n.rotation, rotation):
                    #logging.debug("Can't play tile at this position, has illegal neighbour: %s" % (n))
                    return False

        return True

    def neighbours_for(self, location):
        neighbours = []
        neighbours.append(self.grid.get((location[0], location[1] - 1), (location[0], location[1] - 1)))
        neighbours.append(self.grid.get((location[0], location[1] + 1), (location[0], location[1] + 1)))
        neighbours.append(self.grid.get((location[0] - 1, location[1]), (location[0] - 1, location[1])))
        neighbours.append(self.grid.get((location[0] + 1, location[1]), (location[0] + 1, location[1])))

        return neighbours

    def add_to_board(self, tid, location, rotation):
        assert type(rotation) == int

        if not self.is_legal_on_location(tid, location, rotation):
            raise ValueError("Tile %s is illegal on location: %s with rotation: %s" % (tid, location, rotation))

        # Add ourself, set values
        self._play_tile(tid, location, rotation)

    def playable_locations(self, for_tile=None):
        # if not for a specific tile, return the whole set
        if not for_tile:
            return self.edges
        else:
            # else match
            locations = set()
            for l in self.edges:
                for r in ROTATIONS.values():
                    if self.is_legal_on_location(for_tile, l, ROTATIONS[r]):
                        locations.add(l)
            return locations

    def _play_tile(self, tid, location, rotation):
        # remove location from playable locations
        if location in self.edges:
            self.edges.remove(location)

        # set actual values in the tile
        tile = self.boardtiles[tid]
        tile.location = location
        tile.rotation = rotation
        self.grid[location] = tile
        self.tilesleft.remove(tid)

        # keep track of playable locations
        for n in self.neighbours_for(location):
            # add all neighbours that aren't played tiles == empty locations
            if type(n) is not PlayedTile:
                self.edges.add(n)

        tile = self.boardtiles[tid]
        # second pass, add ourself as neighbours!
        neighbours = self.neighbours_for(location)

        has_neighbours = False
        for n in neighbours:
            if type(n) is PlayedTile:
                tile.neighbours.append(n)
                n.neighbours.append(tile)
                has_neighbours = True

        # add to global entities
        # if there are no neighbours, create entities
#        if not has_neighbours:
#            for pos in tile.tile.positions:
#                assert pos[1] in ROLE_TO_ENTITY
#                entity_type = ROLE_TO_ENTITY[pos[1]]
#                entities_of_type = self.entities.setdefault(entity_type, [])
#                entity = []
#                if pos in tile.tile.position_to_connection:
#                    entity.append((tile.tile.id, tile.tile.position_to_connection[pos]))
#                    entities_of_type.append(entity)
#        else:
#            # else merge with existing or create new
#            for n in neighbours:
#                if type(n) is PlayedTile:
#                    pass

        logging.info("Played tile %s at location %s, rotated %s" % (tid, location, rotation))

    def extremes(self):
        """ Returns the topleft and bottomright corner extreme locations of
        the current board state.
        """
        x = set(e[0] for e in self.edges)
        y = set(e[1] for e in self.edges)
        return (min(x), max(y)), (max(x), min(y))

    def dimensions(self):
        """ Returns the board size that would be needed in order to place
        this board, includes edges.
        """
        e = self.extremes()
        return ((abs(e[0][0]) + 1 + e[1][0]),
                (abs(e[1][1]) + 1 + e[0][1]))

    def __repr__(self):
        return "Played tiles: %d\nTiles left: %s " % ((len(self.boardtiles) - len(self.tilesleft)),
                                                        len(self.tilesleft))