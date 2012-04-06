'''
Created on Mar 10, 2012

@author: anders
'''

import copy
import logging
import simplejson

class UnsupportedOperationException(Exception):
    pass

class Enum(object):

    def __init__(self, *args, **kwargs):
        self.reverse = {}
        for i in xrange(0, len(args)):
            setattr(self, args[i], i)
            self.reverse[i] = args[i]

        setattr(self, 'initialized', True)

    def __setattr__(self, *args, **kwargs):
        if not getattr(self, 'initialized', None):
            super.__setattr__(self, *args, **kwargs)
        else:
            raise UnsupportedOperationException('Enums are immutable')

    def __setitem__(self, *args, **kwargs):
        if not getattr(self, 'initialized', None):
            super.__setitem__(self, *args, **kwargs)
        else:
            raise UnsupportedOperationException('Enums are immutable')

    def __getitem__(self, item):
        return getattr(self, item)

    def __delattr__(self, *args, **kwargs):
        raise UnsupportedOperationException('Enums are immutable')

    def __repr__(self):
        return str(self.reverse)

    def by_ordinal(self, idx):
        assert type(idx) == int
        assert idx >= 0
        assert len(self.reverse) > idx
        return self.reverse[idx]

    def values(self):
        for i in self.reverse.values():
            yield i

VALID_EDGES = set(['top', 'bottom', 'left', 'right'])

def numeric_compare(x, y):
    return int(x) - int(y)

def validate_tileset_config(json, valid_entities):
    """ 
    Validates a json-enoded tileset
    @param json tileset
    @type json json-encoded string
    @param valid_entities set of valid entities for positions
    @type valid_entities set of strings
    """
    assert json is not None

    assert 'tiles' in json, '"tiles" not in tileset'
    assert 'base_tiles' in json, '"base_tiles" not in tileset'

    for name, tile in json['base_tiles'].items():
        logging.debug("Validating base tile: %s" % (name))

        assert 'positions' in tile, 'Error in tile: %s' % (tile)
        assert 'edges' in tile, 'Error in tile: %s' % (tile)
        assert 'connections' in tile, 'Error in tile: %s' % (tile)

        cset = set()
        assert 'edges' in tile, 'Missing edges in tile: %s' % (tile)
        assert type(tile['edges'] == dict), 'Error with edges in tile: %s' % (tile)
        for edge, value in tile['edges'].items():
            assert edge in VALID_EDGES, 'Error with edge loations in tile: %s' % (tile)
            assert 'type' in value, 'Error with edge type in tile: %s' % (tile)
            assert value['type'] in valid_entities, 'Error with edge entity type in tile: %s' % (tile)

            assert 'connections' in value, 'Error with connections with edge in tile: %s' % (tile)
            connections = value['connections']
            assert type(connections) == list, 'Error with connections with edge in tile: %s' % (tile)
            assert len(connections) > 0, 'Error with connections with edge in tile: %s' % (tile)
            for c in connections:
                assert type(c) == str, 'Error with connections with edge in tile: %s' % (tile)
                cset.add(c)

        total_cset = set()
        assert 'connections' in tile, 'Missing connections in tile: %s' % (tile)
        assert type(tile['connections'] == list), 'Error with connections in tile: %s' % (tile)

        assert type(tile['connections'][0] == list), 'Error with connections in tile: %s' % (tile)
        for c in tile['connections']:
            for num in c:
                assert int(num) >= 0, 'Error with values in connections in tile: %s' % (tile)
                assert num in cset, 'Error with values in connections in tile: %s, does not exist in any edge' % (tile)
                total_cset.add(num)

        assert total_cset == cset, 'Error with connections, mismatch, in tile: %s' % (tile)

        assert 'positions' in tile, 'Missing positions in tile: %s' % (tile)
        assert type(tile['positions'] == list), 'Error with positions in tile: %s' % (tile)

        for pos in tile['positions']:
            assert 'x' in pos, 'Error with positions, lacking x coord, in tile: %s' % (tile)
            assert 'y' in pos, 'Error with positions, lacking y coord, in tile: %s' % (tile)

            if 'connection' in pos:
                c = pos['connection']
                assert type(c) == str, 'Invalid connection type in tile: %s' % (tile)
                assert c in cset, 'Invalid position, connction doesnt exist, in tile: %s' % (tile)
    
                x = pos['x']
                assert type(x) == int, 'Invalid coord for position in tile: %s' % (tile)
                assert x >= 0 and x <= 100, 'Invalid coord for position in tile: %s' % (tile)
    
                y = pos['y']
                assert type(y) == int, 'Invalid coord for position in tile: %s' % (tile)
                assert y >= 0 and y <= 100, 'Invalid coord for position in tile: %s' % (tile)

        if 'shield' in tile:
            assert type(tile['shield']) == bool, 'Error with shield in tile: %s' % (tile)

    numbers = [number for number, _ in json['tiles'].items()]
    numbers = sorted(numbers, cmp=numeric_compare)
    for i in xrange(0, len(numbers) - 1):
        assert (int(numbers[i+1]) - int(numbers[i])) == 1, "Error in tile numbering at tile #%d" % (i)

def load_config(filename):
    data = open(filename).read()
    return simplejson.loads(data)