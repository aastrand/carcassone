'''
Created on Mar 10, 2012

@author: anders
'''

import copy
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

    def __init__(self, config, father = None):
        self.positions = []
        self.edges = ['']*4
        self.fields = []

        self.shield = None

        if father:
            self._setup(father)

        self._setup(config)

    def _setup(self, config):
        # Positions for meeples
        self._setup_positions(config['positions'])
        self._setup_edges(config['edges'])
        self._setup_fieldsets(config['fieldsets'])

        # And respect shielded, value = position index
        if 'shield' in config:
            self.shield = config['shield'] if len(config['shield']) > 0 else None  

    def _setup_positions(self, position_config):
        assert position_config is not None
        for position, value in position_config.items():
            self.positions.append((position,value))

    def _setup_edges(self, edge_config):
        assert edge_config is not None
        for edge, value in edge_config.items():
            self.edges[EDGES[edge]] = MATERIALS[value]

    def _setup_fieldsets(self, fieldset_config):
        assert fieldset_config is not None
        for fieldset in fieldset_config:
            s = {}
            map(s.__setitem__, [CORNERS[f] for f in fieldset], [])
            self.fields.append(set(s))

    def __repr__(self):
        return "edges: %s\npositions: %s\nfieldsets: %s\nshielded: %s\n" % (
               str(self.edges),
               str(self.positions),
               str(self.fields),
               str(self.shielded))

    def is_legal_adjecent_to(self, tile, edge, own_rotation, that_rotation):
        my_edge = self.edges[(edge - own_rotation) % 4]
        that_edge = tile.edges[(edge + 2 - that_rotation) % 4]
        return my_edge == that_edge