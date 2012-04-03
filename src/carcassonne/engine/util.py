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
BASE_POSITIONS = ['top-left', 'top', 'top-right', 'middle-left', 'middle', 'middle-right', 'bottom-left', 'bottom', 'bottom-right']

def create_positions(base_positions, depth):
    """ Creates all valid positions for a given subdivision depth.
    Depth == 0 gives us the base positions defined above.
    Depth == 1 gives us additional top-right-right, top-left-left etc etc.
    """
    positions = copy.deepcopy(base_positions)

    for i in xrange(0, depth):
        temp = []

        # Create new subdivisions
        for j in xrange(0, len(base_positions)):
            for k in xrange(0, len(base_positions)):
                temp.append("%s-%s" % (positions[j], base_positions[k]))

        # Add them to the total list
        positions.extend(temp)

    return positions

VALID_POSITIONS = create_positions(BASE_POSITIONS, 1)

def numeric_compare(x, y):
    return int(x) - int(y)

def validate_tileset_config(json, valid_roles, valid_environments):
    """ 
    Validates a json-enoded tileset
    @param json tileset
    @type json json-encoded string
    @param valid_roles set of valid roles for positions
    @type valid_roles set of strings
    """
    assert json is not None
    assert valid_roles is not None and type(valid_roles) == set

    assert 'tiles' in json, '"tiles" not in tileset'

    for number, tile in json['tiles'].items():
        assert 'name' in tile
        logging.debug("Validating tile %s, name: %s" % (number, tile['name']))

        assert 'positions' in tile, 'Error in tile: %s' % (tile)
        assert 'edges' in tile, 'Error in tile: %s' % (tile)
        assert 'connections' in tile, 'Error in tile: %s' % (tile)

        assert 'positions' in tile, 'Missing positions in tile: %s' % (tile)
        assert type(tile['positions'] == dict), 'Error with positions in tile: %s' % (tile)

        for pos, role in tile['positions'] .items():
            assert role in valid_roles, 'Invalid role in tile: %s' % (tile)
            assert pos in VALID_POSITIONS, 'Error with valid positions in tile: %s' % (tile)

        cset = set()
        assert 'edges' in tile, 'Missing edges in tile: %s' % (tile)
        assert type(tile['edges'] == dict), 'Error with edges in tile: %s' % (tile)
        for edge, value in tile['edges'].items():
            assert edge in VALID_EDGES, 'Error with edge loations in tile: %s' % (tile)
            assert 'type' in value, 'Error with edge type in tile: %s' % (tile)
            assert value['type'] in valid_environments, 'Error with edge environment type in tile: %s' % (tile)

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

        if 'shield' in tile:
            assert tile['shield'] in VALID_POSITIONS, 'Error with shield in tile: %s' % (tile)

    numbers = [number for number, _ in json['tiles'].items()]
    numbers = sorted(numbers, cmp=numeric_compare)
    for i in xrange(0, len(numbers) - 1):
        assert (int(numbers[i+1]) - int(numbers[i])) == 1, "Error in tile numbering at tile #%d" % (i)

def load_config(filename):
    data = open(filename).read()
    return simplejson.loads(data)