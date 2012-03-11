'''
Created on Mar 11, 2012

@author: anders
'''
import unittest

import carcassonne.engine.tile as tile

from carcassonne.engine.board import Board, ConfigError
from carcassonne.engine.util import load_config

class BoardTest(unittest.TestCase):

    def setUp(self):
        self.broken_conf = {
                                "base_tiles": {
                                    "starter": {
                                        "positions": {
                                            "top": "knight",
                                            "middle": "thief",
                                            "bottom": "farmer",
                                            "top-left": "farmer"
                                        },
                                        "edges": {
                                            "top": "city",
                                            "right": "road",
                                            "left": "road",
                                            "bottom": "field"
                                        },
                                        "fieldsets": [
                                            ["bottom-right", "bottom-left"],
                                            ["top-left", "top-right"]
                                        ]
                                    },
                                    "cloister": {
                                        "inherits": "cloisterroad",
                                        "positions": {
                                            "middle": "monk",
                                            "bottom-right": "farmer"
                                        },
                                        "edges": {
                                            "top": "field",
                                            "right": "field",
                                            "bottom": "field",
                                            "left": "field"
                                        },
                                        "fieldsets": [
                                            ["top-left", "top-right", "bottom-right", "bottom-left"]
                                        ]
                                    },
                                    "cloisterroad": {
                                        "inherits": "cloister",
                                        "positions": {
                                            "bottom": "thief"
                                        },
                                        "edges": {
                                            "bottom": "road"
                                        }
                                    }
                                },

                                "tiles": {
                                    "1": "starter",
                                    "2": "cloister",
                                    "3": "cloister",
                                    "4": "cloister",
                                    "5": "cloister",
                                    "6": "cloisterroad",
                                    "7": "cloisterroad"
                                }
                            }

        self.override_pos_conf = {
                                    "base_tiles": {
                                        "starter": {
                                            "positions": {
                                                "top": "knight",
                                                "middle": "thief",
                                                "bottom": "farmer",
                                                "top-left": "farmer"
                                            },
                                            "edges": {
                                                "top": "city",
                                                "right": "road",
                                                "left": "road",
                                                "bottom": "field"
                                            },
                                            "fieldsets": [
                                                ["bottom-right", "bottom-left"],
                                                ["top-left", "top-right"]
                                            ]
                                        },
                                        "cloister": {
                                            "positions": {
                                                "middle": "monk",
                                                "bottom": "farmer"
                                            },
                                            "edges": {
                                                "top": "field",
                                                "right": "field",
                                                "bottom": "field",
                                                "left": "field"
                                            },
                                            "fieldsets": [
                                                ["top-left", "top-right", "bottom-right", "bottom-left"]
                                            ]
                                        },
                                        "cloisterroad": {
                                            "inherits": "cloister",
                                            "positions": {
                                                "bottom": "thief",
                                                "bottom-right": "farmer"
                                            },
                                            "edges": {
                                                "bottom": "road"
                                            }
                                        }
                                    },

                                    "tiles": {
                                        "1": "starter",
                                        "2": "cloister",
                                        "3": "cloister",
                                        "4": "cloister",
                                        "5": "cloister",
                                        "6": "cloisterroad",
                                        "7": "cloisterroad"
                                    }
                                }

    def test_setup(self):
        config = load_config('data/vanilla_tileset.json')
        b = Board(config)

        for t in b.boardtiles.values():
            self.assertEquals(len(t.tile.edges), 4, 'Every tile once loaded into the board must have 4 edges: %s' % (t))
            self.assertTrue('' not in t.tile.edges, "Every edge must be filld in: %s" % (t))
            self.assertTrue(len(t.tile.positions) > 0, "Every tile has at least one position: %s" % (t))

            posset = set()
            for pos, _ in t.tile.positions:
                self.assertTrue(pos not in posset, "Multuple positions for same rol in tile %s" % (t))
                posset.add(pos)

    def test_resolve_dep_fail(self):
        try:
            _ = Board(self.broken_conf)
            self.fail("Circular dependencies are illegal")
        except ConfigError:
            pass

    def test_override_pos(self):
        b = Board(self.override_pos_conf)
        self.assertEquals(len(b.boardtiles['6'].tile.positions), 3)

    def test_add_to_board(self):
        b = Board(self.override_pos_conf)
        self.assertEquals(b.grid.get((0, -1), None), None)
        b.add_to_board('2', (0, -1), tile.ROTATIONS.deg0)
        self.assertEquals(b.grid[(0, -1)].tile.name, "cloister")

        self.assertEquals(b.grid.get((1, 0), None), None)
        b.add_to_board('6', (1, 0), tile.ROTATIONS.deg90)
        self.assertEquals(b.grid[(1, 0)].tile.name, "cloisterroad")

        self.assertEquals(b.grid.get((-1, 0), None), None)
        b.add_to_board('7', (-1, 0), tile.ROTATIONS.deg270)
        self.assertEquals(b.grid[(-1, 0)].tile.name, "cloisterroad")

        self.assertEquals(b.grid.get((2, 0), None), None)
        b.add_to_board('4', (2, 0), tile.ROTATIONS.deg180)
        self.assertEquals(b.grid[(2, 0)].tile.name, "cloister")

        # Play an already played tile again, should fail
        try:
            b.add_to_board('2', (0, -1), tile.ROTATIONS.deg0)
            self.fail("Tile should already be played")
        except ValueError, v:
            pass

        # Play another tile, but same pos, should fail
        try:
            b.add_to_board('3', (0, -1), tile.ROTATIONS.deg0)
            self.fail("Location should already be played")
        except ValueError, v:
            pass

        # Mismatch, should fail
        try:
            b.add_to_board('3', (0, 1), tile.ROTATIONS.deg0)
            self.fail("Tile shouldnt fit there (city + field)")
        except ValueError, v:
            pass

        # Crazy position, should fail
        try:
            b.add_to_board('3', (0, 11), tile.ROTATIONS.deg0)
            self.fail("Tile should have no neighbours")
        except ValueError, v:
            pass

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_setup']
    unittest.main()