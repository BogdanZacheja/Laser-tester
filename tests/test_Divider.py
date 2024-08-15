import unittest
from utils.Divider import Divider


class MyTestCase(unittest.TestCase):

    def test_values(self):
        d = Divider()
        values_list = d.values(1,10,6)
        proper_list = [1,2,4,6,8,10]
        self.assertEqual(values_list, proper_list)

    def test_longest(self):
        d = Divider()
        values_list = d.values(1, 10, 6)
        longest = d.find_longest(values_list)
        proper_longest = 2  # Since 10 has 2 digits
        self.assertEqual(longest, proper_longest)

    def test_mid_value(self):
        d = Divider()
        values_list = d.values(1,10,6)
        middle = d.mid_value(values_list)
        proper_middle = 6
        self.assertEqual(middle, proper_middle)
        
    
