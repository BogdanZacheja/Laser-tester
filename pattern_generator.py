from utils import engraving as e, moves as m, Divider as d, EngrCords as r
from utils.plot_file import plot_file


class PatternGenerator:
    """
    A class to generate laser cutting patterns with specified parameters.

    Attributes
    ----------
    file_name : str
        Name of the output G-code file.
    length : float
        Length of each square in the pattern in millimeters.
    width : float
        Width of each square in the pattern in millimeters.
    space : float
        Space between squares in the pattern in millimeters.
    passes_per_mm : int
        Number of laser passes per millimeter.
    x_start_pos : float
        Starting X position for the pattern.
    y_start_pos : float
        Starting Y position for the pattern.
    x_squares : int
        Number of squares along the X-axis.
    y_squares : int
        Number of squares along the Y-axis.
    start_power : int
        Starting laser power.
    end_power : int
        Ending laser power.
    start_feed : int
        Starting feed rate.
    end_feed : int
        Ending feed rate.
    turn_on_g_code : str
        G-code command to turn on the laser.
    turn_off_g_code : str
        G-code command to turn off the laser.

    Methods
    -------
    generate_pattern():
        Generates the complete laser cutting pattern.
    initialize_file():
        Initializes the output file by writing the start coordinates.
    etch_power_speed_values():
        Engraves power and speed values onto the pattern.
    generate_snake_paths():
        Generates the snake paths for the pattern.
    """
    def __init__(self, file_name: str, length: float, width: float, space: float, passes_per_mm: int,
                 x_start_pos: float, y_start_pos: float, x_squares: int, y_squares: int,
                 start_power: int, end_power: int, start_feed: int, end_feed: int,
                 turn_on_g_code: str, turn_off_g_code: str):
        self.file_name = file_name
        self.length = length
        self.width = width
        self.space = space
        self.passes_per_mm = passes_per_mm
        self.x_start_pos = x_start_pos
        self.y_start_pos = y_start_pos
        self.x_squares = x_squares
        self.y_squares = y_squares
        self.start_power = start_power
        self.end_power = end_power
        self.start_feed = start_feed
        self.end_feed = end_feed
        self.turn_on_g_code = turn_on_g_code
        self.turn_off_g_code = turn_off_g_code
        self.loc = m.Location((x_start_pos, y_start_pos), file_name)
        self.power_list = d.Divider().values(start_power, end_power, y_squares)
        self.speed_list = d.Divider().values(start_feed, end_feed, x_squares)

    def generate_pattern(self):
        """
        Generate the complete laser engraving pattern by initializing the file,
        etching power and speed values, and generating the snake paths.
        """
        self.initialize_file()
        self.etch_power_speed_values()
        self.generate_snake_paths()

        plot_file(self.file_name)

    def initialize_file(self):
        """
        Initialize the file by clearing its content and writing the start coordinates.
        """
        self.loc.start(self.file_name)

    def etch_power_speed_values(self):
        """
        Etch power and speed values into the material by generating coordinates
        for each value and engraving the corresponding text.
        """
        characters = e.read_font("fonts/normal.cxf")
        ec = r.EngrCords()

        # Generate engraving coordinates for power and speed values
        engr_coords = ec.engr_coords(self.x_start_pos, self.y_start_pos,
                                     self.width, self.length, self.space,
                                     self.power_list, self.speed_list)
        print("Engraving Coordinates:", engr_coords)

        # Iterate over the generated engraving coordinates
        for key, (x_pos, y_pos) in engr_coords.items():
            text = e.engr_text(str(key[0]), x_pos, y_pos, self.width / 4)

            # Engrave each character of the generated text
            for char, pos in text.items():
                e.engrave(char, pos[0], pos[1], characters, self.file_name,
                          self.width, self.turn_on_g_code, self.turn_off_g_code)

    def generate_snake_paths(self):
        """
        Generates the snake paths for the pattern.

        This method initializes the EngrCords instance, generates the iterator for
        power and speed values, and creates snake paths for each square in the pattern.
        """
        ec = r.EngrCords()
        x_start_patt, y_start_patt = ec.pattern_start(self.x_start_pos, self.y_start_pos,
                                                      self.width, self.length, self.space)

        iterator = iter(m.PowerSpeedIterator(self.y_squares, self.x_squares,
                                             x_start_patt, y_start_patt,
                                             self.width, self.length, self.space,
                                             self.speed_list, self.power_list))
        for _ in range(self.x_squares * self.y_squares):
            x_pos, y_pos, power, speed = iterator.x_pos, iterator.y_pos, iterator.power, iterator.speed
            self.loc.snake_path(x_pos, y_pos, power, speed, self.width, self.length,
                                self.passes_per_mm, self.file_name,
                                self.turn_on_g_code, self.turn_off_g_code)
            next(iterator)

"""
if __name__ == '__main__':
    generator = PatternGenerator(file_name="output.nc", length=10, width=10, space=5, passes_per_mm=3,
                                 x_start_pos=0, y_start_pos=0, x_squares=2, y_squares=2,
                                 start_power=1000, end_power=5000, start_feed=1000, end_feed=5000,
                                 turn_on_g_code='M4', turn_off_g_code='M5')
    generator.generate_pattern()
"""