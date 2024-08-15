import re
from typing import Dict
from math import pi, sin, cos
from decimal import Decimal


def read_font(file: str) -> Dict:
    """
    Read a coordinates for draw all characters using a font
    form cxf file.
    Arc are changing to set of 30 straight lines.

    Data storage structure in cxf file:

    ['character'] 'number of lines with coordinates to draw character'
    'L' means straight line, numbers are line coordinates like bellow:
    L 'begin line in X-axis', 'begin in Y', 'end in X', 'end in Y'

    'A' means part of the circle with structure like bellow:
    A 'circle center in X-axis', 'center in Y', 'radius 'start angle','end angle',

    Example character:
    [N] 7
    L 0.827586,5.793103,0.827586,0
    L 1.103448,5.793103,4.413793,0.551724
    L 1.103448,5.241379,4.413793,0
    L 4.413793,5.793103,4.413793,0
    L 0,5.793103,1.103448,5.793103
    L 3.586207,5.793103,5.241379,5.793103
    L 0,0,1.655172,0

    Parameters
    ----------
    file: str
      Name of cxf file with a font

    Returns
    ---------
    characters: Dict
      Dict contain characters and coordinates for lines necessary
      draw a character
      Dict structure: [character] : [line1], [line2], [line 3]......
    """
    with open(file, "r", encoding="utf-8") as f:
        scale_factor = Decimal('15.0')
        characters = {}
        coords_list = []
        lines_number = 0
        char = None

        for line in f:
            new_char = re.match(r'^\[(.*)]\s+(\d+)', line)
            coord_line = re.match(r'^L (.+)', line)
            arc = re.match(r'^A (.+)', line)
            blank_line = re.match(r'^\s*$', line)

            if new_char:
                char = new_char.group(1)
                lines_number = int(new_char.group(2))

            if coord_line:
                coords = coord_line.group(1)
                coords = [Decimal(n) for n in coords.split(',')]
                coords = [float(n / scale_factor) for n in coords]
                coords = [round(n, 6) for n in coords]  # Round after converting to float
                coords_list.append(coords)
                lines_number -= 1

            if arc:
                coords_arc = arc.group(1)
                coords_arc = [Decimal(n) for n in coords_arc.split(',')]
                x_cen, y_cen, rad, start_angle, end_angle = coords_arc
                x_cen = round(float(x_cen / scale_factor), 6)
                y_cen = round(float(y_cen / scale_factor), 6)
                rad = round(float(rad / scale_factor), 6)

                if end_angle < start_angle:
                    start_angle -= Decimal('360.0')

                steps = int((end_angle - start_angle) / Decimal('30')) + 1
                angl_step = (end_angle - start_angle) / Decimal(steps)

                angle = start_angle
                for i in range(steps):
                    angle += angl_step
                    angle_float = float(angle)
                    x_end = round(cos(angle_float * pi / 180) * rad + x_cen, 6)
                    y_end = round(sin(angle_float * pi / 180) * rad + y_cen, 6)
                    # If you start the next segment at the end of the previous, round these too
                    x_start = round(cos(float(start_angle + i * angl_step) * pi / 180) * rad + x_cen, 6)
                    y_start = round(sin(float(start_angle + i * angl_step) * pi / 180) * rad + y_cen, 6)
                    coords = [x_start, y_start, x_end, y_end]
                    coords_list.append(coords)

                lines_number -= 1

            if lines_number == 0 and blank_line is None:
                characters[char] = coords_list
                coords_list = []

    return characters


def engr_text(word: str, x: float, y: float, size: float) -> Dict:
    """
    Function crate start coordinates for draw each character in word

    Parameters
    ----------
    word: str
      text for engrave
    x: float
      Begin of word in X-axis
    y: float
      Begin of word in Y-axis
    size: float
      Font size in millimeters

    Return
    --------
    line: Dict
      Dictionary with character a start coordinates
      Dict structure [character] : [x_start, y_start]
    """
    line = {}
    x_pos = x
    y_pos = y
    for num, char in enumerate(word):
        line[char + str(num)] = x_pos, y_pos
        x_pos += size * 1.5
    return line


def engrave(char, x, y, font, out_file, size, turn_on, turn_off):
    """
    Function create g code for draw a character.

    Parameters
    ----------
    char: str
      character to draw
    x: float
      start coordinates for draw character
    y: float
      start coordinates for draw character
    font: Dict
      characters dictionary with characters and coordinates
    out_file: str
      name of txt file with g code for engrave
    size: float
      size of font in millimeters
    turn_on: str
      g code command for turn on laser
    turn_off: str
      g code command for turn off
     """
    with open(out_file, 'a') as o:
        o.write(f'G1 X{x} Y{y} \n')
        for line in font[char[0]]:
            x0 = round(float(line[0]) * size, 6)
            y0 = round(float(line[1]) * size, 6)
            x1 = round(float(line[2]) * size, 6)
            y1 = round(float(line[3]) * size, 6)

            o.write(f'G1 X{x + x0} Y{y + y0} \n')
            o.write(f'{turn_on} \n')
            o.write(f'G1 X{x + x1} Y{y + y1} \n')
            o.write(f'{turn_off} \n')

        o.write(f'{turn_off} \n')


# import os
# from utils.plot_file import plot_file
# with open('test.txt', 'a') as o:
#     o.truncate(0)
# text = engr_text('Bogdan-123-BOGDAN', 10, 10, 2)
# cur_path = os.path.dirname(__file__)
# new_path = os.path.relpath('..\\fonts\\normal.cxf', cur_path)
# characters = read_font(new_path)
# for a, c in text.items():
#     print(a[0], c[0], c[1])
#     engrave(a[0], c[0], c[1], characters, 'test.txt', 5, 'M5', 'M4')
# print('end')
# plot_file('test.txt')
