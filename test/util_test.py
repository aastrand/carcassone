'''
Created on Mar 11, 2012

@author: anders
'''
import unittest

import carcassonne.engine.util as util
from carcassonne.engine.util import load_config

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
        json = load_config('data/basic_tileset.json')
        util.validate_tileset_config(json,
                                     set(['city', 'field', 'road']))




if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
