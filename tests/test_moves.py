import unittest
from contextlib import redirect_stdout
from io import StringIO
from utils.moves import Location, PowerSpeedIterator
import os

class TestLocation(unittest.TestCase):
    def test_location_initialization(self):
        loc = Location((0, 0), 'testfile.txt')
        self.assertEqual(loc.x, 0)
        self.assertEqual(loc.y, 0)

    def test_location_repr(self):
        loc = Location((1, 2), 'testfile.txt')
        self.assertEqual(repr(loc), 'Location(x=1, y=2)')

    def test_location_property(self):
        loc = Location((0, 0), 'testfile.txt')
        loc.loc = (10, 20)
        self.assertEqual(loc.loc, (10, 20))

    def test_location_file_write(self):
        loc = Location((0, 0), 'testfile.txt')
        loc.start('testfile.txt')
        with open('testfile.txt', 'r') as f:
            content = f.read()
        self.assertIn('X0 Y0', content)
        os.remove('testfile.txt')

    def test_location_write_power_speed(self):
        loc = Location((0, 0), 'testfile.txt')
        loc.start('testfile.txt')
        loc.write_power_speed('testfile.txt', 1500, 300)
        with open('testfile.txt', 'r') as f:
            lines = f.readlines()
        self.assertIn('S1500 F300', lines[2])
        os.remove('testfile.txt')

    def test_location_snake_path(self):
        loc = Location((0, 0), 'testfile.txt')
        loc.start('testfile.txt')
        loc.snake_path(0, 0, 1000, 500, 10, 10, 10, 'testfile.txt', 'M4', 'M5')
        with open('testfile.txt', 'r') as f:
            content = f.read()
        self.assertIn('M4', content)
        self.assertIn('M5', content)
        os.remove('testfile.txt')


class TestPowerSpeedIterator(unittest.TestCase):
    def test_iterator(self):
        iterator = PowerSpeedIterator(2, 2, 0, 0, 10, 10, 5, [1000, 2000], [100, 200])
        iterator_result = list(iterator)
        expected_result = [
            (15, 0, 200, 1000),
            (0, 15, 100, 2000),
            (15, 15, 200, 2000),
            (0, 30, 100, 1000)
        ]
        self.assertEqual(iterator_result, expected_result)

    def test_iterator_stop_iteration(self):
        iterator = PowerSpeedIterator(1, 1, 0, 0, 10, 10, 5, [100], [1000])
        iter_obj = iter(iterator)
        next(iter_obj)  # This should succeed.
        with self.assertRaises(StopIteration):
            next(iter_obj)

    def test_empty_power_list(self):
        with self.assertRaises(IndexError):
            iterator = PowerSpeedIterator(1, 1, 0, 0, 10, 10, 5, [], [1000])
            list(iterator)

    def test_empty_speed_list(self):
        with self.assertRaises(IndexError):
            iterator = PowerSpeedIterator(1, 1, 0, 0, 10, 10, 5, [100], [])
            list(iterator)


    def test_negative_coordinates(self):
        iterator = PowerSpeedIterator(2, 2, -10, -10, 10, 10, 5, [1000, 2000], [100, 200])
        iterator_result = list(iterator)
        expected_result = [
            (5, -10, 200, 1000),
            (-10, 5, 100, 2000),
            (5, 5, 200, 2000),
            (-10, 20, 100, 1000)
        ]
        self.assertEqual(iterator_result, expected_result)


if __name__ == '__main__':
    unittest.main()
