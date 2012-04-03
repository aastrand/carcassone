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
        self.conf = load_config('data/basic_tileset.json')

    def test_setup(self):
        b = Board(self.conf)

        for t in b.boardtiles.values():
            self.assertEquals(len(t.tile.edges), 4, 'Every tile once loaded into the board must have 4 edges: %s' % (t))
            self.assertTrue('' not in t.tile.edges, "Every edge must be filld in: %s" % (t))
            self.assertTrue(len(t.tile.positions) > 0, "Every tile has at least one position: %s" % (t))

            posset = set()
            for pos, _ in t.tile.positions:
                self.assertTrue(pos not in posset, "Multuple positions for same rol in tile %s" % (t))
                posset.add(pos)

    def test_add_to_board(self):
        b = Board(self.conf)
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
        b = Board(self.conf)
        b.add_to_board('2', (0, -1), tile.ROTATIONS.deg0)

        self.assertTrue(b.is_legal_on_location('6', (1, 0), tile.ROTATIONS.deg90))
        self.assertFalse(b.is_legal_on_location('6', (1, 0), tile.ROTATIONS.deg180))
        self.assertFalse(b.is_legal_on_location('6', (1, 0), tile.ROTATIONS.deg270))
        self.assertFalse(b.is_legal_on_location('6', (1, 0), tile.ROTATIONS.deg0))

    def test_neighbours_for(self):
        b = Board(self.conf)
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
        b = Board(self.conf)
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
        b = Board(self.conf)
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
        b = Board(self.conf)
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

        b = Board(self.conf)
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