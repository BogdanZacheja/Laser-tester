import unittest
from utils.EngrCords import EngrCords

class TestEngrCords(unittest.TestCase):
    def setUp(self):
        self.engr_cords = EngrCords()

    def test_pattern_start(self):
        x_start, y_start = self.engr_cords.pattern_start(0, 0, 10, 10, 5)
        self.assertEqual(x_start, 15)
        self.assertEqual(y_start, 10)

    def test_engr_coords(self):
        # Set up initial parameters.
        x = 0
        y = 0
        width = 10
        length = 10
        space = 5
        pwr_list = [100, 200, 300]
        speed_list = [1000, 2000, 3000]

        sign_dict = self.engr_cords.engr_coords(x, y, width, length, space, pwr_list, speed_list)

        self.assertEqual(sign_dict[(100, 'p')], (15, 0))
        self.assertEqual(sign_dict[(200, 'p')], (30, 0))
        self.assertEqual(sign_dict[(300, 'p')], (45, 0))

        self.assertEqual(sign_dict[(1000, 's')], (0, 15))
        self.assertEqual(sign_dict[(2000, 's')], (0, 30))
        self.assertEqual(sign_dict[(3000, 's')], (0, 45))

    def test_mid_value(self):
        values_list = [10, 20, 30, 40, 50]
        mid_val = self.engr_cords.mid_value(values_list)
        self.assertEqual(mid_val, 30)

        values_list = [1, 3, 5]  # Testing with odd number of elements
        mid_val = self.engr_cords.mid_value(values_list)
        self.assertEqual(mid_val, 3)

        values_list = [2, 4]  # Testing with even number of elements, should return the lower middle
        mid_val = self.engr_cords.mid_value(values_list)
        self.assertEqual(mid_val, 2)
