import unittest
from DataBase import include

class TestDataBase(unittest.TestCase):
    def test_include(self):
        a=['a','b']
        b=['a','b']
        self.assertTrue(include(a,b))
        b += ['c',]
        self.assertTrue(include(a,b))
        a += ['d',]
        self.assertFalse(include(a,b))
    
    