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
    reverse = {}

    def __init__(self, *args, **kwargs):
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

    assert 'base_tiles' in json, '"base_tiles" not in tileset'
    assert 'tiles' in json, '"tiles" not in tileset'

    for name, basetile in json['base_tiles'].items():
        logging.debug("Validating basetile %s" % (name)) 
        assert 'positions' in basetile or 'inherits' in basetile, 'Error in basetile: %s' % (basetile)
        assert 'edges' in basetile or 'inherits' in basetile, 'Error in basetile: %s' % (basetile)
        assert 'fieldsets' in basetile or 'inherits' in basetile, 'Error in basetile: %s' % (basetile)

        if 'positions' in basetile:
            assert type(basetile['positions'] == dict), 'Error with positions in basetile: %s' % (basetile)

            for pos, role in basetile['positions'] .items():
                assert role in valid_roles, 'Invalid role in basetile: %s' % (basetile)
                assert pos in VALID_POSITIONS, 'Error with valid positions in basetile: %s' % (basetile)

        if 'edges' in basetile:
            assert type(basetile['edges'] == dict), 'Error with edges in basetile: %s' % (basetile)
            if "inherits" not in basetile:
                assert len(basetile['edges']) == 4, 'Error with amount of edges in basetile: %s' % (basetile)
            for edge, value in basetile['edges'].items():
                assert edge in VALID_EDGES, 'Error with edge loations in basetile: %s' % (basetile)
                assert value in valid_environments, 'Error with edge environment type in basetile: %s' % (basetile)

        if 'fieldsets' in basetile:
            assert type(basetile['fieldsets'] == list), 'Error with fieldsets in basetile: %s' % (basetile)

            if len(basetile['fieldsets']) > 0:
                assert type(basetile['fieldsets'][0] == list), 'Error with fieldsets in basetile: %s' % (basetile)
                for fset in basetile['fieldsets']:
                    for corner in fset:
                        assert corner in VALID_POSITIONS, 'Error with corner values in fieldsets in basetile: %s' % (basetile)

        if 'shield' in basetile:
            if len(basetile['shield']) > 0:
                assert basetile['shield'] in VALID_POSITIONS, 'Error with shield in basetile: %s' % (basetile)

    numbers = []
    for number, name in json['tiles'].items():
        assert name in json['base_tiles'], "Tile name missing from basetiles: %s" % (name)
        numbers.append(number)

    numbers = sorted(numbers, cmp=numeric_compare)
    for i in xrange(0, len(numbers) - 1):
        assert (int(numbers[i+1]) - int(numbers[i])) == 1, "Error in tile numbering at tile #%d" % (i)

def load_config(filename):
    data = open(filename).read()
    return simplejson.loads(data)