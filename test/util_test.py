'''
Created on Mar 11, 2012

@author: anders
'''
import unittest
import simplejson

import carcassonne.engine.util as util

class UtilTest(unittest.TestCase):

    def test_enum(self):
        empty = util.Enum()

        e = util.Enum('gris', 'svin', 'ko')
        self.assertEquals(e.gris, 0)
        self.assertEquals(e.svin, 1)
        self.assertEquals(e.ko, 2)

        self.assertEquals(e['ko'], e.ko)

        self.assertEquals(e.by_ordinal(0), 'gris')
        self.assertEquals(e.by_ordinal(1), 'svin')
        self.assertEquals(e.by_ordinal(2), 'ko')

        try:
            e['haest'] = 4
            self.fail('Enums should be immutable')
        except util.UnsupportedOperationException:
            pass

        try:
            e.haest = 4
            self.fail('Enums should be immutable')
        except util.UnsupportedOperationException:
            pass

        try:
            del e.ko
            self.fail('Enums should be immutable')
        except util.UnsupportedOperationException:
            pass

    def test_validate(self):
        content = open('data/vanilla_tileset.json').read()
        json_content = simplejson.loads(content)
        util.validate_tileset_config(json_content,
                                     set(['thief', 'knight', 'monk', 'farmer']),
                                     set(['city', 'field', 'road']))

    def test_create_positions(self):
        """ Tests that we can generate the subdivision of positions correctly.
        The base positions (4 directions) can each be split into 4 sub-positions.
        Each of these 4 can also be split .. and so on.
        """
        positions = util.create_positions(util.BASE_POSITIONS, 0)
        self.assertEquals(positions, ['top-left', 'top', 'top-right', 
                                      'middle-left', 'middle', 'middle-right',
                                      'bottom-left', 'bottom', 'bottom-right'])

        positions = util.create_positions(util.BASE_POSITIONS, 1)
        self.assertEquals(positions, ['top-left', 'top', 'top-right', 
                                      'middle-left', 'middle', 'middle-right', 
                                      'bottom-left', 'bottom', 'bottom-right', 
                                      'top-left-top-left', 'top-left-top', 
                                      'top-left-top-right', 'top-left-middle-left', 
                                      'top-left-middle', 'top-left-middle-right', 
                                      'top-left-bottom-left', 'top-left-bottom', 
                                      'top-left-bottom-right', 'top-top-left', 
                                      'top-top', 'top-top-right', 'top-middle-left', 
                                      'top-middle', 'top-middle-right', 'top-bottom-left', 
                                      'top-bottom', 'top-bottom-right', 'top-right-top-left', 
                                      'top-right-top', 'top-right-top-right', 
                                      'top-right-middle-left', 'top-right-middle', 
                                      'top-right-middle-right', 'top-right-bottom-left', 
                                      'top-right-bottom', 'top-right-bottom-right', 
                                      'middle-left-top-left', 'middle-left-top', 
                                      'middle-left-top-right', 'middle-left-middle-left', 
                                      'middle-left-middle', 'middle-left-middle-right', 
                                      'middle-left-bottom-left', 'middle-left-bottom', 
                                      'middle-left-bottom-right', 'middle-top-left', 
                                      'middle-top', 'middle-top-right', 'middle-middle-left', 
                                      'middle-middle', 'middle-middle-right', 
                                      'middle-bottom-left', 'middle-bottom', 
                                      'middle-bottom-right', 'middle-right-top-left', 
                                      'middle-right-top', 'middle-right-top-right', 
                                      'middle-right-middle-left', 'middle-right-middle', 
                                      'middle-right-middle-right', 'middle-right-bottom-left', 
                                      'middle-right-bottom', 'middle-right-bottom-right', 
                                      'bottom-left-top-left', 'bottom-left-top', 
                                      'bottom-left-top-right', 'bottom-left-middle-left', 
                                      'bottom-left-middle', 'bottom-left-middle-right', 
                                      'bottom-left-bottom-left', 'bottom-left-bottom', 
                                      'bottom-left-bottom-right', 'bottom-top-left', 
                                      'bottom-top', 'bottom-top-right', 'bottom-middle-left', 
                                      'bottom-middle', 'bottom-middle-right', 
                                      'bottom-bottom-left', 'bottom-bottom', 
                                      'bottom-bottom-right', 'bottom-right-top-left', 
                                      'bottom-right-top', 'bottom-right-top-right', 
                                      'bottom-right-middle-left', 'bottom-right-middle', 
                                      'bottom-right-middle-right', 'bottom-right-bottom-left', 
                                      'bottom-right-bottom', 'bottom-right-bottom-right'])


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
