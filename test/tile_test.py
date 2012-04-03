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
                                    "top": {"type": "field"},
                                    "bottom": {"type": "field"},
                                    "left": {"type": "field"},
                                    "right": {"type": "field"}
                                },
                               "shield": "top-left"
                            }

        self.topcityroad = {
                                "connections": [
                                    [
                                        "0", 
                                        "1", 
                                        "5"
                                    ], 
                                    [
                                        "2"
                                    ], 
                                    [
                                        "3"
                                    ], 
                                    [
                                        "4"
                                    ]
                                ], 
                                "edges": {
                                    "bottom": {
                                        "connections": [
                                            "2", 
                                            "3", 
                                            "4"
                                        ], 
                                        "type": "road"
                                    }, 
                                    "left": {
                                        "connections": [
                                            "5"
                                        ], 
                                        "type": "city"
                                    }, 
                                    "right": {
                                        "connections": [
                                            "1"
                                        ], 
                                        "type": "city"
                                    }, 
                                    "top": {
                                        "connections": [
                                            "0"
                                        ], 
                                        "type": "city"
                                    }
                                }, 
                                "name": "topcityroad", 
                                "positions": {
                                    "bottom": "thief", 
                                    "bottom-left": "farmer", 
                                    "bottom-right": "farmer", 
                                    "middle": "knight"
                                }
                            }

        self.topcity = {
                                "connections": [
                                    [
                                        "3", 
                                        "0", 
                                        "1"
                                    ], 
                                    [
                                        "2"
                                    ]
                                ], 
                                "edges": {
                                    "bottom": {
                                        "connections": [
                                            "2"
                                        ], 
                                        "type": "field"
                                    }, 
                                    "left": {
                                        "connections": [
                                            "3"
                                        ], 
                                        "type": "city"
                                    }, 
                                    "right": {
                                        "connections": [
                                            "1"
                                        ], 
                                        "type": "city"
                                    }, 
                                    "top": {
                                        "connections": [
                                            "0"
                                        ], 
                                        "type": "city"
                                    }
                                }, 
                                "name": "topcity", 
                                "positions": {
                                    "bottom": "farmer", 
                                    "middle": "knight"
                                }
                            }

        self.crossroads = {
                                "connections": [
                                    [
                                        "0", 
                                        "1", 
                                        "7"
                                    ], 
                                    [
                                        "2"
                                    ], 
                                    [
                                        "5"
                                    ], 
                                    [
                                        "8"
                                    ], 
                                    [
                                        "3", 
                                        "6"
                                    ], 
                                    [
                                        "9", 
                                        "4"
                                    ]
                                ], 
                                "edges": {
                                    "bottom": {
                                        "connections": [
                                            "4", 
                                            "5", 
                                            "6"
                                        ], 
                                        "type": "road"
                                    }, 
                                    "left": {
                                        "connections": [
                                            "7", 
                                            "8", 
                                            "9"
                                        ], 
                                        "type": "road"
                                    }, 
                                    "right": {
                                        "connections": [
                                            "1", 
                                            "2", 
                                            "3"
                                        ], 
                                        "type": "road"
                                    }, 
                                    "top": {
                                        "connections": [
                                            "0"
                                        ], 
                                        "type": "field"
                                    }
                                }, 
                                "name": "crossroads", 
                                "positions": {
                                    "bottom": "thief", 
                                    "bottom-left": "farmer", 
                                    "bottom-right": "farmer", 
                                    "middle-left": "thief", 
                                    "middle-right": "thief", 
                                    "top": "farmer"
                                }
                            }

    def test_tile_instantiation(self):
        t = tile.Tile('grass', self.allgrass_tile)

        self.assertEquals(t.edges, [0, 0, 0, 0], 'All edges should be fields')

        self.assertEquals(len(t.positions), 1)
        self.assertEquals(t.positions[0], ('middle', 'farmer'))

        self.assertEquals(t.shield, "top-left")

        t = tile.Tile('topcityroad', self.topcityroad)

        self.assertEquals(t.edges, [1, 1, 2, 1], 'Bottom edge should be road')

        self.assertEquals(len(t.positions), 4)
        self.assertTrue(('middle', 'knight') in t.positions)
        self.assertTrue(('bottom', 'thief') in t.positions)
        self.assertTrue(('bottom-right', 'farmer') in t.positions)
        self.assertTrue(('bottom-left', 'farmer') in t.positions)

        self.assertEquals(t.shield, None)

    def test_is_legal_adjecent_to(self):
        city = tile.Tile('topcityroad', self.topcityroad)
        grass = tile.Tile('grass', self.allgrass_tile)
        topcity = tile.Tile('topcity', self.topcity)
        crossroads = tile.Tile('crossroads', self.crossroads)

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

    def test_get_edge(self):
        t = tile.Tile('crossroads', self.crossroads)
        self.assertEquals(t.get_edge(tile.EDGES.top, tile.ROTATIONS.deg0), 0)
        self.assertEquals(t.get_edge(tile.EDGES.top, tile.ROTATIONS.deg90), 2)
        self.assertEquals(t.get_edge(tile.EDGES.top, tile.ROTATIONS.deg180), 2)
        self.assertEquals(t.get_edge(tile.EDGES.top, tile.ROTATIONS.deg270), 2)

        self.assertEquals(t.get_edge(tile.EDGES.bottom, tile.ROTATIONS.deg0), 2)
        self.assertEquals(t.get_edge(tile.EDGES.bottom, tile.ROTATIONS.deg90), 2)
        self.assertEquals(t.get_edge(tile.EDGES.bottom, tile.ROTATIONS.deg180), 0)
        self.assertEquals(t.get_edge(tile.EDGES.bottom, tile.ROTATIONS.deg270), 2)

        self.assertEquals(t.get_edge(tile.EDGES.left, tile.ROTATIONS.deg0), 2)
        self.assertEquals(t.get_edge(tile.EDGES.left, tile.ROTATIONS.deg90), 2)
        self.assertEquals(t.get_edge(tile.EDGES.left, tile.ROTATIONS.deg180), 2)
        self.assertEquals(t.get_edge(tile.EDGES.left, tile.ROTATIONS.deg270), 0)

        self.assertEquals(t.get_edge(tile.EDGES.right, tile.ROTATIONS.deg0), 2)
        self.assertEquals(t.get_edge(tile.EDGES.right, tile.ROTATIONS.deg90), 0)
        self.assertEquals(t.get_edge(tile.EDGES.right, tile.ROTATIONS.deg180), 2)
        self.assertEquals(t.get_edge(tile.EDGES.right, tile.ROTATIONS.deg270), 2)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
