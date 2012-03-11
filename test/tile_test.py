'''
Created on Mar 11, 2012

@author: anders
'''
import unittest
import copy
import carcassonne.engine.tile as tile

class TileTest(unittest.TestCase):

    def setUp(self):
        self.allgrass_tile = {
                                "positions": {
                                    "middle": "farmer"
                                },
                                "edges": {
                                    "top": "field",
                                    "bottom": "field",
                                    "left": "field",
                                    "right": "field"
                                },
                                "fieldsets": [
                                    [
                                        "top-left",
                                        "top-right",
                                        "bottom-left",
                                        "bottom-right"
                                    ]
                                ],
                               "shield": "top-left"
                            }

        self.topcityroad = {
                                "inherits": "topcity",
                                "positions": {
                                    "top": "knight",
                                    "bottom": "thief",
                                    "bottom-left": "farmer",
                                    "bottom-right": "farmer",
                                },
                                "edges": {
                                    "bottom": "road"
                                },
                                "fieldsets": [
                                    [
                                        "bottom-left"
                                    ],
                                    [
                                        "bottom-right"
                                    ]
                                ]
                            }

        self.topcity = {
                                "positions": {
                                    "top": "knight",
                                    "bottom": "farmer"
                                },
                                "edges": {
                                    "top": "city",
                                    "bottom": "field",
                                    "left": "city",
                                    "right": "city"
                                },
                                "shield": "",
                                "fieldsets": [
                                    [
                                        "bottom-left", "bottom-right"
                                    ]
                                ]
                            }

        self.crossroads = {
                                "positions": {
                                    "top": "farmer",
                                    "left": "thief",
                                    "right": "thief",
                                    "bottom": "thief",
                                    "bottom-right": "farmer",
                                    "bottom-left": "farmer"
                                },
                                "edges": {
                                    "top": "field",
                                    "left": "road",
                                    "right": "road",
                                    "bottom": "road"
                                },
                                "fieldsets": [
                                    [
                                        "top-left",
                                        "top-right"
                                    ],
                                    [
                                        "bottom-right"
                                    ],
                                    [
                                        "bottom-left"
                                    ]
                                ]
                            }

    def test_tile_instantiation(self):
        t = tile.Tile(self.allgrass_tile)

        self.assertEquals(t.edges, [0, 0, 0, 0], 'All edges should be fields')

        self.assertEquals(len(t.positions), 1)
        self.assertEquals(t.positions[0], ('middle', 'farmer'))

        self.assertEquals(len(t.fields), 1)
        self.assertEquals(t.fields[0], set([3, 2, 1, 0]))

        self.assertEquals(t.shield, "top-left")

    def test_tile_fieldsets(self):
        t = tile.Tile(self.topcityroad)

        self.assertEquals(t.edges, ['', '', 2, ''], 'Bottom edge should be road')

        self.assertEquals(len(t.positions), 4)
        self.assertTrue(('top', 'knight') in t.positions)
        self.assertTrue(('bottom', 'thief') in t.positions)
        self.assertTrue(('bottom-right', 'farmer') in t.positions)
        self.assertTrue(('bottom-left', 'farmer') in t.positions)

        self.assertEquals(len(t.fields), 2)
        self.assertTrue(set([2]) in t.fields)
        self.assertTrue(set([3]) in t.fields)

        self.assertEquals(t.shield, None)

    def test_is_legal_adjecent_to(self):
        city = tile.Tile(self.topcityroad)
        grass = tile.Tile(self.allgrass_tile)
        topcity = tile.Tile(self.topcity)
        crossroads = tile.Tile(self.crossroads)

        baseval = [False]*4*4*4
        self._all_combos(city, grass, baseval)

        vals = copy.deepcopy(baseval)
        # Rotate city 180 degrees and put other on top = ok
        vals[8] = True 
        # Rotate city 180 degrees, grass 90 and put other on top = ok
        vals[9] = True 
        # Rotate city 180 degrees, grass 180 and put other on top = ok
        vals[10] = True 
        # Rotate city 180 degrees, grass 270 and put other on top = ok
        vals[11] = True 

        # Rotate city 270 degrees and put other to the right = ok
        vals[28] = True 
        # Rotate city 270 degrees, grass 90 and put other to the right = ok
        vals[29] = True 
        # Rotate city 270 degrees, grass 180 and put other to the right = ok
        vals[30] = True 
        # Rotate city 270 degrees, grass 270 and put other to the right = ok
        vals[31] = True 

        # Grass below city = ok
        vals[32] = True
        # Grass 90 deg rotated below city = ok
        vals[33] = True
        # Grass 180 deg roteated below city = ok
        vals[34] = True
        # Grass 270 deg rotated below city = ok
        vals[35] = True

        # Rotate city 90 degrees and put other to the left = ok
        vals[52] = True
        # Rotate city 90 degrees, grass 90 and put other to the left = ok
        vals[53] = True
        # Rotate city 90 degrees, grass 180 and put other to the left = ok
        vals[54] = True
        # Rotate city 90 degrees, grass 270 and put other to the left = ok
        vals[55] = True

        self._all_combos(topcity, grass, vals)

        vals = copy.deepcopy(baseval)

        # Rotate city 180, crossroads 180, put crossraods on top of city
        vals[10] = True
        # Rotate city 270, crossroads 270, put crossraods to the right of city
        vals[31] = True
        # Put crossraods below city
        vals[32] = True
        #  Rotate city 90, crossroads 90, put crossraods to the left of city
        vals[53] = True

        self._all_combos(topcity, crossroads, vals)

    def _all_combos(self, t1, t2, vals):
        # Try all combinations of edge-choice and rotations of both tiles
        # 4 * 4 * 4 = 64 combos
        i = 0
        for edge in xrange(0, 4):
            for rot1 in xrange(0, 4):
                for rot2 in xrange(0, 4):
                    self.assertEquals(t1.is_legal_adjecent_to(t2, edge, rot1, rot2), vals[i])
                    i += 1

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
