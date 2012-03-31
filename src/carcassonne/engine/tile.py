'''
Created on Mar 10, 2012

@author: anders
'''

from carcassonne.engine.util import Enum

# TODO: make expansion aware
MATERIALS = Enum('field', 'city', 'road', 'cloister')
ROLES = Enum('farmer', 'knight', 'thief', 'monk')
EDGES = Enum('top', 'right', 'bottom', 'left')
CORNERS = Enum('top-left', 'top-right', 'bottom-right', 'bottom-left')
ROTATIONS = Enum('deg0', 'deg90', 'deg180', 'deg270')

class TileConfigException(Exception):
    pass

class Tile(object):

    def __init__(self, name, config, father=None):
        self.name = name
        self.positions = []
        self.edges = ['']*4
        self.fields = []

        self.shield = None

        if father:
            self._copy_from(father)

        self._setup(config)

    def _setup(self, config):
        # Positions for meeples
        if 'positions' in config:
            self._setup_positions(config['positions'])
        if 'edges' in config:
            self._setup_edges(config['edges'])
        if 'fieldsets' in config:
            self._setup_fieldsets(config['fieldsets'])

        # And respect shielded, value = position index
        if 'shield' in config:
            self.shield = config['shield'] if len(config['shield']) > 0 else None  

    def _setup_positions(self, position_config):
        for position, value in position_config.items():
            for spos, srole in self.positions:
                if position == spos:
                    self.positions.remove((spos, srole))
            self.positions.append((position,value))

    def _setup_edges(self, edge_config):
        for edge, value in edge_config.items():
            self.edges[EDGES[edge]] = MATERIALS[value]

    def _setup_fieldsets(self, fieldset_config):
        # Reset fields
        self.fields = []

        for fieldset in fieldset_config:
            s = {}
            map(s.__setitem__, [CORNERS[f] for f in fieldset], [])
            self.fields.append(set(s))

    def _copy_from(self, tile):
        # Ugly n^2 here, but very short lists so it's ok
        for pos, role in tile.positions:
            for spos, srole in self.positions:
                if spos == pos:
                    break
            else:
                self.positions.append((pos, role))

        for idx, e in enumerate(tile.edges):
            self.edges[idx] = e

        for f in tile.fields:
            self.fields.append(f)

    def __repr__(self):
        return "%s:\nedges: %s\npositions: %s\nfieldsets: %s\nshielded: %s\n" % (
               self.name,
               str(self.edges),
               str(self.positions),
               str(self.fields),
               str(self.shield))

    def is_legal_adjecent_to(self, tile, edge, own_rotation, that_rotation):
        my_edge = self.get_edge(edge, own_rotation)
        that_edge = tile.get_edge(edge + 2, that_rotation)
        return my_edge == that_edge

    def get_edge(self, edge, rotation):
        return self.edges[(edge - rotation) % 4]
