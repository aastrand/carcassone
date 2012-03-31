'''
Created on Mar 31, 2012

@author: anders
'''
from carcassonne.engine.tile import ROTATIONS

class Renderer(object):
    @staticmethod
    def render():
        raise NotImplementedError()

    @staticmethod
    def tile_to_id(tile):
        return '%s%s%s%s' % (tile.tile.name, tile.location[0], tile.location[1], tile.rotation) 

    @staticmethod
    def table_pos_to_grid(column, row, board):
        topleft, bottomright = board.extremes()
        c = column + topleft[0]
        r = topleft[1] - row
        return c, r

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
            row = []

            for c in xrange(0,cols+1):
                cg, rg = HtmlRenderer.table_pos_to_grid(c, r, board)
                tile = board.grid.get((cg, rg))

                if tile:
                    rowtext = '<td><img src="data/images/%s.png" id="%s"></td>' % (tile.tile.name,
                                                                                   HtmlRenderer.tile_to_id(tile))
                else:
                    rowtext = '<td></td>' 

                row.append(rowtext)

            rowtexts.append('<tr>%s</tr>' % ('\n'.join(row)))

        table = '<table border="0">\n%s\n</table>' % ('\n'.join(rowtexts))

        return "<body>\n%s\n%s\n</body>" % (js, table)

