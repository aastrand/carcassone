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

    def __init__(self, id, name, config):
        self.id = id
        self.name = name
        self.positions = []
        self.edges = ['']*4
        self.connection_to_edge = {}
        self.edge_to_connections = {}
        self.connections = []
        self.connection_lookup = {}

        self.shield = None

        self._setup(config)

    def _setup(self, config):
        # Positions for meeples
        assert 'connections' in config
        self._setup_connections(config['connections'])
        assert 'edges' in config
        self._setup_edges(config['edges'])
        assert 'positions' in config
        self._setup_positions(config['positions'])

        # And respect shielded, value = position index
        if 'shield' in config:
            self.shield = config['shield']

    def _setup_connections(self, connection_config):
        for connections in connection_config:
            c = []
            self.connections.append(c)
            for conn in connections:
                c.append(conn)
                self.connection_lookup[conn] = c

    def _setup_edges(self, edge_config):
        for edge, value in edge_config.items():
            self.edges[EDGES[edge]] = MATERIALS[value['type']]
            for c in value['connections']:
                self.connection_to_edge[c] = EDGES[edge]
                conns = self.edge_to_connections.setdefault(EDGES[edge], [])
                conns.append(c)

    def _setup_positions(self, position_config):
        for position in position_config:
            self.positions.append(position)

    def __repr__(self):
        return "%s:\nedges: %s\npositions: %s\nshielded: %s\n" % (
               self.name,
               str(self.edges),
               str(self.positions),
               str(self.shield))

    def is_legal_adjecent_to(self, tile, edge, own_rotation, that_rotation):
        my_edge = self.get_edge(edge, own_rotation)
        that_edge = tile.get_edge(edge + 2, that_rotation)
        return my_edge == that_edge

    def get_edge(self, edge, rotation):
        return self.edges[(edge - rotation) % 4]

