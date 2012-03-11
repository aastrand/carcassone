'''
Created on Mar 11, 2012

@author: anders
'''

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
        self._setup_tiles(config['base_tiles'], config['tiles'])

    def _setup_tiles(self, base_tiles, tiles):
        self.boardtiles = {}
        self.grid = {}
        self.tilesleft = set()
        self.reverse = {}

        tileset = [(tid, name) for tid, name in tiles.items()]
        tileset = sorted(tileset, cmp=compare_tileset)

        last_size = -1
        # Resolve dependencies .. reduce tileset and loop until empty
        while len(tileset) > 0:
            for tid, name in tileset:
                father = None
                # Has father? Copy from it
                if "inherits" in base_tiles[name]:
                    fathername = base_tiles[name]['inherits']
                    if fathername in self.reverse:
                        father = self.reverse[fathername][0].tile
                    else:
                        break

                self.boardtiles[tid] = PlayedTile(Tile(name, base_tiles[name], father), [])
                self.reverse.setdefault(name, []).append(self.boardtiles[tid])
                self.tilesleft.add(tid)

                tileset.remove((tid, name))

            if last_size == len(tileset):
                raise ConfigError("ERROR: Could not reduce dependencies in tileset: %s" % (tileset))

            last_size = len(tileset)

        self.root = self.boardtiles['1']
        self._play_tile('1', (0,0), ROTATIONS.deg0)


    def add_to_board(self, tid, location, rotation):
        assert type(rotation) == int

        if tid not in self.tilesleft:
            raise ValueError("Tile %s is already played" % (tid))

        if location in self.grid:
            raise ValueError("Location %s, %s is already occupied" % (location))

        tile = self.boardtiles[tid]

        # Get top, bottom, left, right tiles .. if any
        neighbours = []
        neighbours.append(self.grid.get((location[0], location[1] - 1), None))
        neighbours.append(self.grid.get((location[0], location[1] + 1), None))
        neighbours.append(self.grid.get((location[0] - 1, location[1]), None))
        neighbours.append(self.grid.get((location[0] + 1, location[1]), None))

        # Check if it's ok
        all_none = True
        for n in neighbours:
            if n is not None:
                all_none = False
                edge = relative_pos_to_edge(n.location, location)
                if not n.tile.is_legal_adjecent_to(tile.tile, edge, n.rotation, rotation):
                    raise ValueError("Can't play tile at this position, has illegal neighbour: %s" % (n))

        if all_none:
            raise ValueError("Can't play at this location, no neighbours exist: %s, %s" % (location))

        # Add ourself, set values
        self._play_tile(tid, location, rotation)

        # Second pass, add ourself as neighbours!
        for n in neighbours:
            if n is not None:
                n.neighbours.append(tile)

    def _play_tile(self, tid, location, rotation):
        tile = self.boardtiles[tid]
        tile.location = location
        tile.rotation = rotation
        self.grid[location] = tile
        self.tilesleft.remove(tid)
