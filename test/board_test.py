'''
Created on Mar 11, 2012

@author: anders
'''
import unittest

import carcassonne.engine.tile as tile

from carcassonne.engine.board import Board, ConfigError, PlayedTile
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

        self.full_game_conf = {
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
                                    },
                                    "allcity": {
                                        "positions": {
                                            "middle": "knight"
                                        },
                                        "edges": {
                                            "top": "city",
                                            "bottom": "city",
                                            "left": "city",
                                            "right": "city"
                                        },
                                        "shield": "top-left",
                                        "fieldsets": []
                                    },
                                    "topcity": {
                                        "inherits": "allcity",
                                        "positions": {
                                            "bottom": "farmer"
                                        },
                                        "edges": {
                                            "bottom": "field"
                                        },
                                        "shield": "",
                                        "fieldsets": [
                                            ["bottom-left", "bottom-right"]
                                        ]
                                    },
                                    "topcityshielded": {
                                        "inherits": "topcity",
                                        "shield": "top-left"
                                    },
                                    "topcityroad": {
                                        "inherits": "topcity",
                                        "positions": {
                                            "top": "knight",
                                            "bottom": "thief",
                                            "bottom-left": "farmer",
                                            "bottom-right": "farmer"
                                        },
                                        "edges": {
                                            "bottom": "road"
                                        },
                                        "fieldsets": [
                                            ["bottom-left"],
                                            ["bottom-right"]
                                        ]
                                    },
                                    "topcityroadshielded": {
                                        "inherits": "topcityroad",
                                        "shield": "top-left"
                                    },
                                    "topleftcity": {
                                        "positions": {
                                            "top-left": "knight",
                                            "bottom-right": "farmer"
                                        },
                                        "edges": {
                                            "top": "city",
                                            "right": "field",
                                            "bottom": "field",
                                            "left": "city"
                                        },
                                        "fieldsets": [
                                            ["top-right", "bottom-right", "bottom-left"]
                                        ]
                                    },
                                    "topleftcityshielded": {
                                        "inherits": "topleftcity",
                                        "shield": "top-left"
                                    },
                                    "topleftcityroad": {
                                        "positions": {
                                            "bottom": "thief",
                                            "middle": "farmer",
                                            "bottom-right": "farmer"
                                        },
                                        "edges": {
                                            "top": "city",
                                            "right": "road",
                                            "bottom": "road",
                                            "left": "city"
                                        },
                                        "fieldsets": [
                                            ["top-right", "bottom-left"],
                                            ["bottom-right"]
                                        ]
                                    },
                                    "topleftcityroadshielded": {
                                        "inherits": "topleftcityroad",
                                        "shield": "top-left"
                                    },
                                    "middlecity": {
                                        "positions": {
                                            "middle": "knight",
                                            "top": "farmer",
                                            "bottom": "farmer"
                                        },
                                        "edges": {
                                            "top": "field",
                                            "right": "city",
                                            "bottom": "field",
                                            "left": "city"
                                        },
                                        "fieldsets": [
                                            ["top-left", "top-right"],
                                            ["bottom-left", "bottom-right"]
                                        ]
                                    },
                                    "middlecityshielded": {
                                        "inherits": "middlecity",
                                        "shield": "middle-right"
                                    },
                                    "topleftcornercity": {
                                        "inherits": "topleftcity" 
                                    },
                                    "topbottomcity": {
                                        "positions": {
                                            "top": "knight",
                                            "middle": "farmer",
                                            "bottom": "knight"
                                        },
                                        "edges": {
                                            "top": "city",
                                            "right": "field",
                                            "bottom": "city",
                                            "left": "field"
                                        },
                                        "fieldsets": [
                                            ["top-left", "top-right", "bottom-right", "bottom-left"]
                                        ]
                                    },
                                    "toponeedgecity": {
                                        "positions": {
                                            "top": "knight",
                                            "bottom-right": "farmer"
                                        },
                                        "edges": {
                                            "top": "city",
                                            "right": "field",
                                            "bottom": "field",
                                            "left": "field"
                                        },
                                        "fieldsets": [
                                            ["top-left", "top-right", "bottom-right", "bottom-left"]
                                        ]
                                    },
                                    "toponeedgecityroadturnleft": {
                                        "inherits": "toponeedgecity",
                                        "positions": {
                                            "bottom": "thief"
                                        },
                                        "edges": {
                                            "left": "road",
                                            "bottom": "road"
                                        },
                                        "fieldsets": [
                                            ["top-left", "top-right", "bottom-right"],
                                            ["bottom-left"]
                                        ]
                                    },
                                    "toponeedgecityroadturnright": {
                                        "inherits": "toponeedgecity",
                                        "positions": {
                                            "bottom": "thief"
                                        },
                                        "edges": {
                                            "right": "road",
                                            "bottom": "road"
                                        },
                                        "fieldsets": [
                                            ["top-left", "top-right", "bottom-left"],
                                            ["bottom-right"]
                                        ]
                                    },
                                    "toponeedgecitycrossroads": {
                                        "inherits": "toponeedgecity",
                                        "positions": {
                                            "bottom": "thief",
                                            "middle-right": "thief",
                                            "middle-left": "thief"
                                        },
                                        "edges": {
                                            "right": "road",
                                            "left": "road",
                                            "bottom": "road"
                                        },
                                        "fieldsets": [
                                            ["top-left", "top-right"],
                                            ["bottom-right", "bottom-left"]
                                        ]
                                    },
                                    "toponeedgecityroadmiddle": {
                                        "positions": {
                                            "bottom": "farmer",
                                            "middle": "thief",
                                            "top": "knight"
                                        },
                                        "edges": {
                                            "top": "city",
                                            "right": "road",
                                            "left": "road",
                                            "bottom": "field"
                                        },
                                        "fieldsets": [
                                            ["top-left", "top-right"],
                                            ["bottom-right"],
                                            ["bottom-left"]
                                        ]
                                    },
                                    "topmiddlebottomroad": {
                                        "positions": {
                                            "middle": "thief",
                                            "middle-left": "farmer",
                                            "middle-right": "farmer"
                                        },
                                        "edges": {
                                            "top": "road",
                                            "bottom": "road",
                                            "right": "field",
                                            "left": "field"
                                        },
                                        "fieldsets": [
                                            ["top-left", "bottom-left"],
                                            ["bottom-right", "top-right"]
                                        ]
                                    },
                                    "leftturnroad": {
                                        "positions": {
                                            "middle": "thief",
                                            "top-right": "farmer",
                                            "bottom-left": "farmer"
                                        },
                                        "edges": {
                                            "top": "field",
                                            "bottom": "road",
                                            "right": "field",
                                            "left": "road"
                                        },
                                        "fieldsets": [
                                            ["top-left", "bottom-right", "top-right"],
                                            ["bottom-left"]
                                        ]
                                    },
                                    "crossroads": {
                                        "positions": {
                                            "top": "farmer",
                                            "middle-left": "thief",
                                            "middle-right": "thief",
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
                                            ["top-left", "top-right"],
                                            ["bottom-right"],
                                            ["bottom-left"]
                                        ]
                                    },
                                    "allcrossroads": {
                                        "inherits": "crossroads",
                                        "positions": {
                                            "top": "thief",
                                            "top-left": "farmer",
                                            "top-right": "farmer"
                                        },
                                        "edges": {
                                            "top": "road"
                                        },
                                        "fieldsets": [
                                            ["top-left"],
                                            ["top-right"],
                                            ["bottom-right"],
                                            ["bottom-left"]
                                        ]
                                    }
                                },
                            
                                "tiles": {
                                    "1": "starter",
                                    "2": "cloister",
                                    "3": "cloister",
                                    "4": "cloister",
                                    "5": "cloister",
                                    "6": "cloisterroad",
                                    "7": "cloisterroad",
                                    "8": "allcity",
                                    "9": "topcityshielded",
                                    "10": "topcity",
                                    "11": "topcity",
                                    "12": "topcity",
                                    "13": "topcityroad",
                                    "14": "topcityroadshielded",
                                    "15": "topcityroadshielded",
                                    "16": "topleftcity",
                                    "17": "topleftcity",
                                    "18": "topleftcity",
                                    "19": "topleftcityshielded",
                                    "20": "topleftcityshielded",
                                    "21": "topleftcityroad",
                                    "22": "topleftcityroad",
                                    "23": "topleftcityroad",
                                    "24": "topleftcityroadshielded",
                                    "25": "topleftcityroadshielded",
                                    "26": "middlecity",
                                    "27": "middlecityshielded",
                                    "28": "middlecityshielded",
                                    "29": "topleftcornercity",
                                    "30": "topleftcornercity",
                                    "31": "topbottomcity",
                                    "32": "topbottomcity",
                                    "33": "topbottomcity",
                                    "34": "toponeedgecity",
                                    "35": "toponeedgecity",
                                    "36": "toponeedgecity",
                                    "37": "toponeedgecity",
                                    "38": "toponeedgecity",
                                    "39": "toponeedgecityroadturnleft",
                                    "40": "toponeedgecityroadturnleft",
                                    "41": "toponeedgecityroadturnleft",
                                    "42": "toponeedgecityroadturnright",
                                    "43": "toponeedgecityroadturnright",
                                    "44": "toponeedgecityroadturnright",
                                    "45": "toponeedgecitycrossroads",
                                    "46": "toponeedgecitycrossroads",
                                    "47": "toponeedgecitycrossroads",
                                    "48": "toponeedgecityroadmiddle",
                                    "49": "toponeedgecityroadmiddle",
                                    "50": "toponeedgecityroadmiddle",
                                    "50": "topmiddlebottomroad",
                                    "51": "topmiddlebottomroad",
                                    "52": "topmiddlebottomroad",
                                    "53": "topmiddlebottomroad",
                                    "54": "topmiddlebottomroad",
                                    "55": "topmiddlebottomroad",
                                    "56": "topmiddlebottomroad",
                                    "57": "topmiddlebottomroad",
                                    "58": "leftturnroad",
                                    "59": "leftturnroad",
                                    "60": "leftturnroad",
                                    "61": "leftturnroad",
                                    "62": "leftturnroad",
                                    "63": "leftturnroad",
                                    "64": "leftturnroad",
                                    "65": "leftturnroad",
                                    "66": "leftturnroad",
                                    "67": "crossroads",
                                    "68": "crossroads",
                                    "69": "crossroads",
                                    "70": "crossroads",
                                    "71": "allcrossroads"
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

    def test_is_legal_on_location(self):
        b = Board(self.override_pos_conf)
        b.add_to_board('2', (0, -1), tile.ROTATIONS.deg0)

        self.assertTrue(b.is_legal_on_location('6', (1, 0), tile.ROTATIONS.deg90))
        self.assertFalse(b.is_legal_on_location('6', (1, 0), tile.ROTATIONS.deg180))
        self.assertFalse(b.is_legal_on_location('6', (1, 0), tile.ROTATIONS.deg270))
        self.assertFalse(b.is_legal_on_location('6', (1, 0), tile.ROTATIONS.deg0))

    def test_neighbours_for(self):
        b = Board(self.override_pos_conf)
        b.add_to_board('2', (0, -1), tile.ROTATIONS.deg0)

        n = b.neighbours_for((0,0))
        self.assertEquals(type(n[0]), PlayedTile)
        self.assertEquals(type(n[1]), tuple)
        self.assertEquals(type(n[2]), tuple)
        self.assertEquals(type(n[3]), tuple)

        n = b.neighbours_for((0,-1))
        self.assertEquals(type(n[0]), tuple)
        self.assertEquals(type(n[1]), PlayedTile)
        self.assertEquals(type(n[2]), tuple)
        self.assertEquals(type(n[3]), tuple)

        n = b.neighbours_for((10,10))
        self.assertTrue(all(type(l) is tuple for l in n))

    def test_playable_locations(self):
        b = Board(self.override_pos_conf)
        l = b.playable_locations()
        self.assertEquals(len(l), 4)

        # can only play cloister below starter
        l = b.playable_locations('2')
        self.assertEquals(len(l), 1)
        self.assertEquals(l.pop(), (0, -1))

        b.add_to_board('2', (0, -1), tile.ROTATIONS.deg0)
        l = b.playable_locations()
        # remove 1, add 3 => 6
        self.assertEquals(len(l), 6)

    def test_dimensions(self):
        b = Board(self.override_pos_conf)
        self.assertEquals(b.dimensions(), (3,3))

        b.add_to_board('2', (0, -1), tile.ROTATIONS.deg0)
        self.assertEquals(b.dimensions(), (3,4))

        b.add_to_board('6', (1, 0), tile.ROTATIONS.deg90)
        self.assertEquals(b.dimensions(), (4,4))

        b.add_to_board('7', (-1, 0), tile.ROTATIONS.deg270)
        self.assertEquals(b.dimensions(), (5,4))

        b.add_to_board('4', (2, 0), tile.ROTATIONS.deg180)
        self.assertEquals(b.dimensions(), (6,4))

    def test_extremes(self):
        b = Board(self.override_pos_conf)
        self.assertEquals(b.extremes(), ((-1,1), (1,-1)))

        b.add_to_board('2', (0, -1), tile.ROTATIONS.deg0)
        self.assertEquals(b.extremes(), ((-1,1), (1,-2)))

        b.add_to_board('6', (1, 0), tile.ROTATIONS.deg90)
        self.assertEquals(b.extremes(), ((-1,1), (2,-2)))

        b.add_to_board('7', (-1, 0), tile.ROTATIONS.deg270)
        self.assertEquals(b.extremes(), ((-2,1), (2,-2)))

        b.add_to_board('4', (2, 0), tile.ROTATIONS.deg180)
        self.assertEquals(b.extremes(), ((-2,1), (3,-2)))

    def test_impossible_play(self):
        """From actual random output:
        INFO:root:Played tile 1 at location (0, 0), rotated 0
        INFO:root:Played tile 58 at location (-1, 0), rotated 2
        INFO:root:Played tile 17 at location (-1, -1), rotated 2
        INFO:root:Played tile 29 at location (-2, -1), rotated 0
        INFO:root:Played tile 9 at location (0, -1), rotated 2
        INFO:root:Played tile 28 at location (1, -1), rotated 0
        INFO:root:Played tile 43 at location (1, -2), rotated 1
        INFO:root:Played tile 61 at location (-2, -2), rotated 0
        DEBUG:root:Could not play tile 2, Played tiles: 8
        """

        b = Board(self.full_game_conf)
        b.add_to_board('58', (-1, 0), tile.ROTATIONS.deg180)
        b.add_to_board('17', (-1, -1), tile.ROTATIONS.deg180)
        b.add_to_board('29', (-2, -1), tile.ROTATIONS.deg0)
        b.add_to_board('9', (0, -1), tile.ROTATIONS.deg180)
        b.add_to_board('28', (1, -1), tile.ROTATIONS.deg0)
        b.add_to_board('43', (1, -2), tile.ROTATIONS.deg90)
        b.add_to_board('61', (-2, -2), tile.ROTATIONS.deg0)

        # no playable positions for the cloister now:
        self.assertEquals(b.playable_locations('2'), set())

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_setup']
    unittest.main()