'''
Created on Mar 11, 2012

@author: anders
'''
import unittest

import carcassonne.engine.tile as tile
import carcassonne.engine.util as util

from carcassonne.engine.board import Board, ConfigError, PlayedTile
from carcassonne.render.render import HtmlRenderer, Renderer
from carcassonne.engine.util import load_config

class RenderTest(unittest.TestCase):

    def setUp(self):
        self.conf = load_config('data/basic_tileset.json')

    def test_tile_to_id(self):
        b = Board(self.conf)
        self.assertEquals(Renderer.tile_to_id(b.grid[(0,0)]), 'starter000')

        b.add_to_board('2', (0, -1), tile.ROTATIONS.deg0)
        self.assertEquals(Renderer.tile_to_id(b.grid[(0,-1)]), 'cloister0-10')

    def test_table_pos_to_grid(self):
        b = Board(self.conf)
        b.add_to_board('2', (0, -1), tile.ROTATIONS.deg0)
        b.add_to_board('6', (1, 0), tile.ROTATIONS.deg90)
        b.add_to_board('7', (-1, 0), tile.ROTATIONS.deg270)
        b.add_to_board('4', (2, 0), tile.ROTATIONS.deg180)
        self.assertEquals(Renderer.table_pos_to_grid(0, 0, b), (-1, 0))
        self.assertEquals(Renderer.table_pos_to_grid(3, 0, b), (2, 0))

    def test_pos_to_tile_xy(self):
        pos = {'x' : 20, 'y': 30}
        x, y = Renderer.pos_to_tile_xy(pos, 0)
        self.assertTrue(x >= 0)
        self.assertTrue(y >= 0)
        self.assertTrue(x <= Renderer.tile_width)
        self.assertTrue(x <= Renderer.tile_height)

    def test_rotate(self):
        self.assertEquals(Renderer.rotate(0, 0, 0), (0, 0))
        self.assertEquals(Renderer.rotate(0, 0, 90), (87, 1))
        self.assertEquals(Renderer.rotate(0, 0, 180), (88, 85))
        self.assertEquals(Renderer.rotate(0, 0, 270), (2, 87))
        self.assertEquals(Renderer.rotate(44, 44, 0), (44, 44))
        self.assertEquals(Renderer.rotate(44, 44, 90), (43, 43))
        self.assertEquals(Renderer.rotate(44, 44, 180), (44, 42))
        self.assertEquals(Renderer.rotate(44, 44, 270), (45, 43))
        self.assertEquals(Renderer.rotate(88, 88, 0), (88, 88))
        self.assertEquals(Renderer.rotate(88, 88, 90), (1, 87))
        self.assertEquals(Renderer.rotate(88, 88, 180), (0, 1))
        self.assertEquals(Renderer.rotate(88, 88, 270), (88, 1))

    def test_html_render(self):
        b = Board(self.conf)
        b.add_to_board('2', (0, -1), tile.ROTATIONS.deg0)
        b.add_to_board('6', (1, 0), tile.ROTATIONS.deg90)
        b.add_to_board('7', (-1, 0), tile.ROTATIONS.deg270)
        b.add_to_board('4', (2, 0), tile.ROTATIONS.deg180)

        h = HtmlRenderer.render(b)
        # TODO: assert

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_setup']
    unittest.main()