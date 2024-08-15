from contextlib import contextmanager
from typing import Tuple, List


class Location:
    """
    Class for handling tool localization in the x, y-axis
    and methods to save tool positions and other commands
    in a txt file.
    """

    def __init__(self, coord: Tuple[float, float], file_name: str):
        self.x, self.y = coord
        self.file_name = file_name

    @property
    def loc(self) -> Tuple[float, float]:
        return (self.x, self.y)

    @loc.setter
    def loc(self, loc: Tuple[float, float]):
        self.x, self.y = loc

    @loc.deleter
    def loc(self):
        self.x = self.y = 0

    def __repr__(self) -> str:
        return f'{type(self).__name__}(x={self.x}, y={self.y})'

    @contextmanager
    def open_file(self, name: str):
        """
        Context manager for working with txt files.
        """
        f = open(name, 'a')
        try:
            yield f
        finally:
            f.close()

    def start(self, file: str):
        """
        Clear a file and write start coordinates.

        Parameters
        ----------
        file: str
            Name of the file to be used.
        """
        with self.open_file(file) as f:
            f.truncate(0)
            f.write(f'X{self.x} Y{self.y} \n')
            f.write('G1 F100 S1000\n')

    def write_pos(self, file: str):
        """
        Write current position to file.

        Parameters
        ----------
        file: str
            Name of the file to be used.
        """
        with self.open_file(file) as f:
            f.write(f'G1 X{self.x} Y{self.y} \n')

    def write_power_speed(self, file: str, power: int, speed: int):
        """
        Write power and speed to file.

        Parameters
        ----------
        file: str
            Name of the file to be used.
        power: int
            Power value for the laser.
        speed: int
            Tool speed value.
        """
        with self.open_file(file) as f:
            f.write(f'S{power} F{speed} \n')

    def write(self, file: str, command: str):
        """
        Write a command to the file.

        Parameters
        ----------
        file: str
            Name of the file to be used.
        command: str
            G-code command to write.
        """
        with self.open_file(file) as f:
            f.write(f'G1 {command} \n')

    def snake_path(self, x_start: float, y_start: float, power: int, speed: int, width: float,
                   length: float, passes_per_mm: int, file: str, turn_on: str, turn_off: str):
        """
        Create tool path to burn a square with given speed and power.

        Parameters
        ----------
        x_start: float
            Start tool position on the x-axis.
        y_start: float
            Start tool position on the y-axis.
        power: int
            Power of the laser for the current square.
        speed: int
            Tool speed for the current square.
        width: float
            Width of the burned square.
        length: float
            Length of the burned square.
        passes_per_mm: int
            Number of passes per millimeter.
        file: str
            Name of the file to write the commands to.
        turn_on: str
            G-code command to turn on the laser.
        turn_off: str
            G-code command to turn off the laser.
        """
        self.loc = (x_start, y_start)
        self.write_pos(file)
        self.write_power_speed(file, power, speed)
        print(f'G1 S{power} F{speed}')
        steps = int((length * passes_per_mm) / 2)
        with open(file, 'a') as f:
            for _ in range(steps):
                f.write(f'{turn_on} \n')
                self.x += width
                f.write(f'G1 X{self.x} Y{self.y} \n')
                f.write(f'{turn_off} \n')
                self.y += 1 / passes_per_mm
                f.write(f'G1 X{self.x} Y{self.y} \n')
                f.write(f'{turn_on} \n')
                self.x -= width
                f.write(f'G1 X{self.x} Y{self.y} \n')
                f.write(f'{turn_off} \n')
                self.y += 1 / passes_per_mm
                f.write(f'G1 X{self.x} Y{self.y} \n')
            f.write(f'{turn_off} \n')


class PowerSpeedIterator:
    """
    Iterator to create a grid of tool power, tool speed, and coordinates of
    every burned square. In the next columns, tool power increases.
    In the next rows, tool speed increases.

    Parameters
    ----------
    col_number: int
        Number of grid columns.
    row_number: int
        Number of grid rows.
    x_start: float
        Start tool position on the x-axis.
    y_start: float
        Start tool position on the y-axis.
    length: float
        Length of the burned squares.
    width: float
        Width of the burned squares.
    space: float
        Space between burned squares.
    power_list: List[int]
        List with tool power values for each column.
    speed_list: List[int]
        List with tool speed values for each row.

    Returns
    -------
    Tuple[float, float, int, int]
        Tuple containing the x position, y position, power value, and speed value
        for the current square.
    """

    def __init__(self, col_number: int, row_number: int, x_start: float,
                 y_start: float, length: float,  width: float, space: float,
                 speed_list: List, power_list: List):

        self.col_number = col_number
        self.row_number = row_number
        self.x_start = x_start
        self.y_start = y_start
        self.width = width
        self.length = length
        self.space = space
        self.speed_list = speed_list
        self.power_list = power_list

    def __iter__(self):
        self.row_counter = 0
        self.col_counter = 0
        self.power = self.power_list[self.col_counter]
        self.speed = self.speed_list[self.row_counter]
        self.x_pos = self.x_start
        self.y_pos = self.y_start

        return self

    def __next__(self):
        if self.row_counter >= self.row_number:
            raise StopIteration

        result = f"G1 S{self.speed} F{self.power}"

        self.x_pos += self.space + self.width
        if self.col_counter >= self.col_number - 1:
            self.x_pos = self.x_start
            self.y_pos += self.space + self.length
            self.col_counter = 0
            self.row_counter += 1
        else:
            self.col_counter += 1

        self.power = self.power_list[self.col_counter % len(self.power_list)]
        self.speed = self.speed_list[self.row_counter % len(self.speed_list)]

        return self.x_pos, self.y_pos, self.power, self.speed
