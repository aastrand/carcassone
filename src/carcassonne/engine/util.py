'''
Created on Mar 10, 2012

@author: anders
'''

""" Validates a json-enoded tileset
    @param json tileset
    @type json json-encoded string
    @param valid_roles set of valid roles for positions
    @type valid_roles set of strings
    """
def validate_tileset_config(json, valid_roles):
    assert json is not None
    assert valid_roles is not None and type(valid_roles) == set

    assert 'base_tiles' in json, '"base_tiles" not in tileset'
    assert 'tiles' in json, '"tiles" not in tileset'

    for _, basetile in json['base_tiles'].items():
        assert 'positions' in basetile or 'inherits' in basetile, 'Error in basetile: %s' % (basetile)
        assert 'edges' in basetile or 'inherits' in basetile, 'Error in basetile: %s' % (basetile)
        assert 'fieldsets' in basetile or 'inherits' in basetile, 'Error in basetile: %s' % (basetile)

        if 'positions' in basetile:
            assert type(basetile['positions'] == dict), 'Error in basetile: %s' % (basetile)

            for p in basetile['positions'] .values():
                assert p in valid_roles, 'Error in basetile: %s' % (basetile)

        if 'edges' in basetile:
            assert type(basetile['edges'] == dict), 'Error in basetile: %s' % (basetile)

        if 'fieldsets' in basetile:
            assert type(basetile['fieldsets'] == list), 'Error in basetile: %s' % (basetile)

            if len(basetile['fieldsets']) > 0:
                assert type(basetile['fieldsets'][0] == list), 'Error in basetile: %s' % (basetile)

        if 'shield' in basetile:
            for v in basetile['shield'].values():
                assert v in ['True', 'False'], 'Error in basetile: %s' % (basetile)