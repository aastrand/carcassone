'''
Created on Mar 31, 2012

@author: anders
'''
import math

from carcassonne.engine.tile import ROTATIONS

class Renderer(object):
    tile_width = 88
    tile_height = 86

    offset = int(tile_width*0.1)

    base_pos_to_coord = {'top': offset,
                         'middle': tile_height / 2,
                         'bottom': tile_height - offset,
                         'left': offset,
                         'right': tile_width - offset}

    @staticmethod
    def render():
        raise NotImplementedError()

    @staticmethod
    def tile_to_id(tile):
        return '%s%s%s%s' % (tile.tile.name, tile.location[0], tile.location[1], tile.rotation) 

    @staticmethod
    def table_pos_to_grid(column, row, board):
        topleft, bottomright = board.extremes()
        c = column + topleft[0] + 1
        r = topleft[1] - row - 1
        return c, r

    @staticmethod
    def pos_to_tile_xy(pos, rotation):
        x = int(float(pos['x']) / 100.0 *  float(Renderer.tile_width)) 
        y = int(float(pos['y']) / 100.0 * float(Renderer.tile_height)) 

        rot = ROTATIONS.by_ordinal(rotation)
        angle = int(rot[3:])
        x, y = Renderer.rotate(x, y, angle)

        return x, y

    @staticmethod
    def rotate(x, y, angle):
        assert type(x) == int
        assert type(y) == int
        assert type(angle) == int

        if angle == 0:
            return x, y

        r = math.radians(angle)
        # normalize
        x_n = float(x - Renderer.tile_width/2)
        y_n = float(y - Renderer.tile_height/2)

        x_new = abs(int(x_n * math.cos(r) - y_n * math.sin(r)) + Renderer.tile_width/2)
        y_new = abs(int(x_n * math.sin(r) + y_n * math.cos(r)) + Renderer.tile_height/2)

        return x_new, y_new


class HtmlRenderer(Renderer):
    @staticmethod
    def render(board):
        head = HtmlRenderer._render_head(board)
        body = HtmlRenderer._render_body(board)

        return "<html>\n%s\n%s\n</html>" % (head, body)

    @staticmethod
    def _render_head(board):
        meta = '<meta http-equiv="content-type" content="text/html; charset=UTF-8">'
        title = '<title>carcasonne board construction sample</title>'
        jquery = '<script type="text/javascript" src="http://code.jquery.com/jquery-1.7.1.js"></script>'

        images = []
        for tile in board.grid.values():
            if tile.rotation != 0:
                images.append('$("#%s").rotate(%s);' % (HtmlRenderer.tile_to_id(tile),
                                                        HtmlRenderer._rotation_to_deg(ROTATIONS.by_ordinal(tile.rotation))))

        rotation = """<script type='text/javascript'>//<![CDATA[ 
$(window).load(function(){
%s
});//]]>  
</script>""" % ('\n'.join(images))

        return "<head>\n%s\n%s\n%s\n%s\n</head>" % (meta, title, jquery, rotation)

    @staticmethod
    def _rotation_to_deg(rot):
        return rot.replace('deg', '')

    @staticmethod
    def _render_body(board):
        js = '<script type="text/javascript" src="http://jqueryrotate.googlecode.com/svn/trunk/jQueryRotate.js"></script>'
        cols, rows = board.dimensions()

        rowtexts = []
        for r in xrange(0,rows+1):
            for c in xrange(0,cols+1):
                cg, rg = HtmlRenderer.table_pos_to_grid(c, r, board)
                tile = board.grid.get((cg, rg))

                if tile:
                    #for pos in tile.tile.positions:
                    for pos in tile.tile.positions:
                        x, y = Renderer.pos_to_tile_xy(pos, tile.rotation)
                        rowtexts.append('<div style="position: fixed; top: %dpx; left: %dpx; width: 1x; height: 1px; z-index:200"><img src="data/images/thief.png"></div>' % (y-8+((r)*Renderer.tile_width), (x-8+((c)*Renderer.tile_height))))
                    rowtexts.append('<div style="position: fixed; top: %dpx; left: %dpx; width: 90x; height: 90px; z-index:100"><img src="data/images/%s.png" id="%s"></div>' % ((r)*Renderer.tile_width, (c)*Renderer.tile_height, tile.tile.name, HtmlRenderer.tile_to_id(tile)))

        return "<body>\n%s\n%s\n</body>" % (js, '\n'.join(rowtexts))
