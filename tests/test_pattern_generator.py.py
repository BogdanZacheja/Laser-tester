import unittest
from unittest.mock import patch, MagicMock
from pattern_generator import PatternGenerator


class TestPatternGenerator(unittest.TestCase):

    @patch('pattern_generator.m.Location')
    @patch('pattern_generator.d')
    @patch('pattern_generator.e')
    @patch('pattern_generator.r.EngrCords')
    @patch('pattern_generator.plot_file')
    def test_generate_pattern(self, mock_plot_file, mock_EngrCords, mock_engraving, mock_divider, mock_location):
        # Mock the Location class
        mock_loc_instance = mock_location.return_value
        mock_loc_instance.start = MagicMock()
        mock_loc_instance.snake_path = MagicMock()

        # Mock the Divider class
        mock_divider_instance = mock_divider.Divider.return_value
        mock_divider_instance.values.side_effect = [
            [100, 200, 300, 400, 500],  # Power values
            [1000, 2000, 3000, 4000]    # Speed values
        ]

        # Mock the engraving functions
        mock_engraving.read_font.return_value = {'A': [(0, 0, 1, 1)]}
        mock_engraving.engr_text.return_value = {'A0': (0, 0)}
        mock_engraving.engrave = MagicMock()

        # Mock EngrCords class
        mock_ec_instance = mock_EngrCords.return_value
        mock_ec_instance.engr_coords.return_value = {
            (100, 'p'): (0, 0),
            (200, 'p'): (1, 0),
            (300, 'p'): (2, 0),
            (400, 'p'): (3, 0),
            (500, 'p'): (4, 0)
        }
        mock_ec_instance.pattern_start.return_value = (0, 0)

        # Create an instance of PatternGenerator
        generator = PatternGenerator(
            file_name="output.nc", length=10, width=10, space=5, passes_per_mm=10,
            x_start_pos=0, y_start_pos=0, x_squares=4, y_squares=5,
            start_power=100, end_power=500, start_feed=1000, end_feed=4000,
            turn_on_g_code='M4', turn_off_g_code='M5'
        )

        # Call the generate_pattern method
        generator.generate_pattern()

        # Assertions
        mock_loc_instance.start.assert_called_once_with("output.nc")
        self.assertEqual(mock_loc_instance.snake_path.call_count, 20)
        mock_plot_file.assert_called_once_with("output.nc")

    @patch('pattern_generator.m.Location')
    def test_initialize_file(self, mock_location):
        mock_loc_instance = mock_location.return_value
        generator = PatternGenerator(
            file_name="output.nc", length=10, width=10, space=5, passes_per_mm=10,
            x_start_pos=0, y_start_pos=0, x_squares=4, y_squares=5,
            start_power=100, end_power=500, start_feed=1000, end_feed=4000,
            turn_on_g_code='M4', turn_off_g_code='M5'
        )
        generator.initialize_file()
        mock_loc_instance.start.assert_called_once_with("output.nc")

    @patch('pattern_generator.e')
    @patch('pattern_generator.r.EngrCords')
    def test_etch_power_speed_values(self, mock_EngrCords, mock_engraving):
        mock_engraving.read_font.return_value = {'A': [(0, 0, 1, 1)]}
        mock_engraving.engr_text.return_value = {'A0': (0, 0)}
        mock_engraving.engrave = MagicMock()

        mock_ec_instance = mock_EngrCords.return_value
        mock_ec_instance.engr_coords.return_value = {
            (100, 'p'): (0, 0),
            (200, 'p'): (1, 0),
            (300, 'p'): (2, 0),
            (400, 'p'): (3, 0),
            (500, 'p'): (4, 0)
        }
        mock_ec_instance.pattern_start.return_value = (0, 0)

        generator = PatternGenerator(
            file_name="output.nc", length=10, width=10, space=5, passes_per_mm=10,
            x_start_pos=0, y_start_pos=0, x_squares=4, y_squares=5,
            start_power=100, end_power=500, start_feed=1000, end_feed=4000,
            turn_on_g_code='M4', turn_off_g_code='M5'
        )
        generator.etch_power_speed_values()
        mock_engraving.read_font.assert_called_once_with("fonts/normal.cxf")
        mock_ec_instance.engr_coords.assert_called_once()
        self.assertEqual(mock_engraving.engrave.call_count, 5)

    @patch('pattern_generator.m.Location')
    @patch('pattern_generator.r.EngrCords')
    def test_generate_snake_paths(self, mock_EngrCords, mock_location):
        mock_loc_instance = mock_location.return_value
        mock_loc_instance.snake_path = MagicMock()

        mock_ec_instance = mock_EngrCords.return_value
        mock_ec_instance.pattern_start.return_value = (0, 0)

        generator = PatternGenerator(
            file_name="output.nc", length=10, width=10, space=5, passes_per_mm=10,
            x_start_pos=0, y_start_pos=0, x_squares=4, y_squares=5,
            start_power=100, end_power=500, start_feed=1000, end_feed=4000,
            turn_on_g_code='M4', turn_off_g_code='M5'
        )
        generator.generate_snake_paths()
        self.assertEqual(mock_loc_instance.snake_path.call_count, 20)


if __name__ == '__main__':
    unittest.main()
