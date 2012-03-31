'''
Created on Mar 11, 2012

@author: anders
'''
import unittest

import carcassonne.engine.tile as tile

from carcassonne.engine.board import Board, ConfigError, PlayedTile
from carcassonne.render.render import HtmlRenderer, Renderer

class RenderTest(unittest.TestCase):

    def setUp(self):
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

    def test_tile_to_id(self):
        b = Board(self.override_pos_conf)
        self.assertEquals(Renderer.tile_to_id(b.grid[(0,0)]), 'starter000')

        b.add_to_board('2', (0, -1), tile.ROTATIONS.deg0)
        self.assertEquals(Renderer.tile_to_id(b.grid[(0,-1)]), 'cloister0-10')

    def test_table_pos_to_grid(self):
        b = Board(self.override_pos_conf)
        b.add_to_board('2', (0, -1), tile.ROTATIONS.deg0)
        b.add_to_board('6', (1, 0), tile.ROTATIONS.deg90)
        b.add_to_board('7', (-1, 0), tile.ROTATIONS.deg270)
        b.add_to_board('4', (2, 0), tile.ROTATIONS.deg180)
        self.assertEquals(Renderer.table_pos_to_grid(0, 0, b), (-2, 1))

    def test_html_render(self):
        b = Board(self.override_pos_conf)
        b.add_to_board('2', (0, -1), tile.ROTATIONS.deg0)
        b.add_to_board('6', (1, 0), tile.ROTATIONS.deg90)
        b.add_to_board('7', (-1, 0), tile.ROTATIONS.deg270)
        b.add_to_board('4', (2, 0), tile.ROTATIONS.deg180)

        #h = HtmlRenderer.render(b)
        #print h

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_setup']
    unittest.main()