import unittest
from utils import engraving as e
import os
import filecmp


class MyTestCase(unittest.TestCase):
    def test_engr_text(self):
        text = e.engr_text('ABC123', 0, 0, 4)
        text_prop = {'A0': (0, 0), 'B1': (6.0, 0), 'C2': (12.0, 0), '13': (18.0, 0), '24': (24.0, 0), '35': (30.0, 0)}
        self.assertEqual(text, text_prop)

    def test_read_font(self):
        test_dir = os.path.dirname(__file__)
        font_file = os.path.join(test_dir, 'test_font.cxf')
        self.assertTrue(os.path.exists(font_file), f"Test font file {font_file} does not exist")
        char = e.read_font(font_file)

        a_coord = char['A']
        b_coord = char['B']
        a_coord_converted = [[float(value) for value in line] for line in char['A']]
        b_coord_converted = [[float(value) for value in line] for line in char['B']]

        a_prop = [
            [0.0, 0.0, 0.2, 0.6],
            [0.2, 0.6, 0.4, 0.0],
            [0.055554, 0.166667, 0.344446, 0.166667]]
        b_prop = [
            [0.0, 0.0, 0.0, 0.6],
            [0.0, 0.6, 0.166667, 0.6],
            [0.166667, 0.333334, 0.224518, 0.346538],
            [0.224518, 0.346538, 0.270911, 0.383535],
            [0.270911, 0.383535, 0.296657, 0.436998],
            [0.296657, 0.436998, 0.296657, 0.496336],
            [0.296657, 0.496336, 0.270911, 0.549799],
            [0.270911, 0.549799, 0.224518, 0.586796],
            [0.224518, 0.586796, 0.166667, 0.6],
            [0.0, 0.333333, 0.173332, 0.333333],
            [0.333332, 0.173333, 0.321153, 0.234562],
            [0.321153, 0.234562, 0.286469, 0.28647],
            [0.286469, 0.28647, 0.234561, 0.321154],
            [0.234561, 0.321154, 0.173332, 0.333333],
            [0.333333, 0.173333, 0.333333, 0.16],
            [0.173332, 0.0, 0.234561, 0.012179],
            [0.234561, 0.012179, 0.286469, 0.046863],
            [0.286469, 0.046863, 0.321153, 0.098771],
            [0.321153, 0.098771, 0.333332, 0.16],
            [0.173332, 0.0, 0.0, 0.0]
        ]
        self.assertEqual(a_coord_converted, a_prop)
        self.assertEqual(b_coord_converted, b_prop)

    def test_engrave_single_character(self):
        char = 'A'
        x = 0
        y = 0
        font = {'A': [[0, 0, 1, 1]]}  # Simplified font for testing
        output_file = 'test_output.txt'
        size = 2
        turn_on = 'M3'
        turn_off = 'M5'

        # Ensure the output file is empty or doesn't exist before testing
        if os.path.exists(output_file):
            os.remove(output_file)

        e.engrave(char, x, y, font, output_file, size, turn_on, turn_off)

        # Verify the contents of the output file
        with open(output_file, 'r') as f:
            content = f.read()

        # Check for the presence and order of G-code commands
        self.assertTrue(turn_on + ' \n' in content, f"{turn_on} command not found in output")
        self.assertTrue(turn_off + ' \n' in content, f"{turn_off} command not found in output")
        # Additional checks can be added here to verify the sequence and correctness of the G-code

        # Clean up (delete the test output file)
        os.remove(output_file)


if __name__ == '__main__':
    unittest.main()
