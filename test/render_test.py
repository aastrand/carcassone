'''
Created on Mar 11, 2012

@author: anders
'''
import unittest

import carcassonne.engine.tile as tile

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
        self.assertEquals(Renderer.table_pos_to_grid(0, 0, b), (-2, 1))

    def test_html_render(self):
        b = Board(self.conf)
        b.add_to_board('2', (0, -1), tile.ROTATIONS.deg0)
        b.add_to_board('6', (1, 0), tile.ROTATIONS.deg90)
        b.add_to_board('7', (-1, 0), tile.ROTATIONS.deg270)
        b.add_to_board('4', (2, 0), tile.ROTATIONS.deg180)

        h = HtmlRenderer.render(b)
        self.assertEquals(h, """<html>
<head>
<meta http-equiv="content-type" content="text/html; charset=UTF-8">
<title>carcasonne board construction sample</title>
<script type="text/javascript" src="http://code.jquery.com/jquery-1.7.1.js"></script>
<script type='text/javascript'>//<![CDATA[ 
$(window).load(function(){
$("#cloisterroad101").rotate(90);
$("#cloisterroad-103").rotate(270);
$("#cloister202").rotate(180);
});//]]>  
</script>
</head>
<body>
<script type="text/javascript" src="http://jqueryrotate.googlecode.com/svn/trunk/jQueryRotate.js"></script>
<table border="0">
<tr><td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td></tr>
<tr><td></td>
<td><img src="data/images/cloisterroad.png" id="cloisterroad-103"></td>
<td><img src="data/images/starter.png" id="starter000"></td>
<td><img src="data/images/cloisterroad.png" id="cloisterroad101"></td>
<td><img src="data/images/cloister.png" id="cloister202"></td>
<td></td>
<td></td></tr>
<tr><td></td>
<td></td>
<td><img src="data/images/cloister.png" id="cloister0-10"></td>
<td></td>
<td></td>
<td></td>
<td></td></tr>
<tr><td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td></tr>
<tr><td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td></tr>
</table>
</body>
</html>""")

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_setup']
    unittest.main()