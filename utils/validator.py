from cerberus import Validator


def validate(file_name, length, width, space, passes_per_mm,
             x_start_pos, y_start_pos, x_squares, y_squares,
             start_power, end_power, start_feed, end_feed,
             turn_on_g_code, turn_off_g_code):
    """
    Function to validate inputs for the laser_pattern function.

    Parameters
    ----------
    file_name: str
        Name of the output file.
    length: float
        Length of the pattern.
    width: float
        Width of the pattern.
    space: float
        Space between the elements.
    passes_per_mm: int
        Number of passes per millimeter.
    x_start_pos: float
        Starting position on the x-axis.
    y_start_pos: float
        Starting position on the y-axis.
    x_squares: int
        Number of squares in the x-direction.
    y_squares: int
        Number of squares in the y-direction.
    start_power: int
        Starting power level.
    end_power: int
        Ending power level.
    start_feed: int
        Starting feed rate.
    end_feed: int
        Ending feed rate.
    turn_on_g_code: str
        G-code command to turn on the laser.
    turn_off_g_code: str
        G-code command to turn off the laser.

    Returns
    -------
    errors: dict
        Dictionary containing error messages from Cerberus validation, if any.
    """

    schema = {
        'file_name': {'type': 'string'},
        'length': {'type': 'float', 'min': 0},
        'width': {'type': 'float', 'min': 0},
        'space': {'type': 'float'},
        'passes_per_mm': {'type': 'integer', 'min': 0},
        'x_start_pos': {'type': 'float'},
        'y_start_pos': {'type': 'float'},
        'x_squares': {'type': 'integer', 'min': 0},
        'y_squares': {'type': 'integer', 'min': 0},
        'start_power': {'type': 'integer', 'min': 0},
        'end_power': {'type': 'integer', 'min': 0},
        'start_feed': {'type': 'integer', 'min': 0},
        'end_feed': {'type': 'integer', 'min': 0},
        'turn_on_g_code': {'type': 'string'},
        'turn_off_g_code': {'type': 'string'},
    }

    input_data = {
        'file_name': file_name,
        'length': length,
        'width': width,
        'space': space,
        'passes_per_mm': passes_per_mm,
        'x_start_pos': x_start_pos,
        'y_start_pos': y_start_pos,
        'x_squares': x_squares,
        'y_squares': y_squares,
        'start_power': start_power,
        'end_power': end_power,
        'start_feed': start_feed,
        'end_feed': end_feed,
        'turn_on_g_code': turn_on_g_code,
        'turn_off_g_code': turn_off_g_code,
    }

    v = Validator(schema)
    if not v.validate(input_data):
        return v.errors
    return {}

