import unittest
from utils.validator import validate

class TestValidateFunction(unittest.TestCase):

    def test_valid_input(self):
        """Test the function with valid inputs."""
        valid_input = ('valid_filename.txt', 10.0, 5.0, 1.0, 10, 0.0, 0.0, 5, 5, 50, 100, 500, 1500, 'M3', 'M5')
        self.assertEqual(validate(*valid_input), {}, "Expected no errors for valid inputs")

    def test_invalid_file_name_type(self):
        """Test with an invalid file name type (not a string)."""
        invalid_input = (123, 10.0, 5.0, 1.0, 10, 0.0, 0.0, 5, 5, 50, 100, 500, 1500, 'M3', 'M5')
        self.assertNotEqual(validate(*invalid_input), {}, "Expected an error for invalid file name type")

    def test_negative_length(self):
        """Test with a negative length."""
        invalid_input = ('valid_filename.txt', -10.0, 5.0, 1.0, 10, 0.0, 0.0, 5, 5, 50, 100, 500, 1500, 'M3', 'M5')
        self.assertNotEqual(validate(*invalid_input), {}, "Expected an error for negative length")

    def test_invalid_start_power_value(self):
        """Test with an invalid start_power value (negative integer)."""
        invalid_input = ('valid_filename.txt', 10.0, 5.0, 1.0, 10, 0.0, 0.0, 5, 5, -50, 100, 500, 1500, 'M3', 'M5')
        self.assertNotEqual(validate(*invalid_input), {}, "Expected an error for invalid start_power value")

    def test_invalid_turn_on_g_code_type(self):
        """Test with an invalid turn_on_g_code type (not a string)."""
        invalid_input = ('valid_filename.txt', 10.0, 5.0, 1.0, 10, 0.0, 0.0, 5, 5, 50, 100, 500, 1500, 123, 'M5')
        self.assertNotEqual(validate(*invalid_input), {}, "Expected an error for invalid turn_on_g_code type")

    def test_zero_length(self):
        """Test with zero length."""
        valid_input = ('valid_filename.txt', 0.0, 5.0, 1.0, 10, 0.0, 0.0, 5, 5, 50, 100, 500, 1500, 'M3', 'M5')
        self.assertEqual(validate(*valid_input), {}, "Expected no error for zero length")

    def test_missing_required_field(self):
        """Test with missing required field (file_name not provided)."""
        # Assuming you adjust your function to handle missing fields scenario
        invalid_input = (None, 10.0, 5.0, 1.0, 10, 0.0, 0.0, 5, 5, 50, 100, 500, 1500, 'M3', 'M5')
        self.assertNotEqual(validate(*invalid_input), {}, "Expected an error for missing required field")
