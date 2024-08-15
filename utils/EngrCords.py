from typing import List, Dict, Tuple


class EngrCords:
    """
    Class for generating engraving coordinates.
    Attributes
    ----------
    y_start : float
        Starting Y position for the engraving pattern.
    x_start : float
        Starting X position for the engraving pattern.
    sign_dict : dict
        Dictionary to store power/speed values and their corresponding coordinates.
    sign_coords : list
        List to store coordinates for engraving.
    """
    def __init__(self):
        self.y_start = None
        self.x_start = None
        self.sign_dict = {}
        self.sign_coords = []

    def engr_coords(self, x: float, y: float, width: float, length: float, space: float, pwr_list: List[int], speed_list: List[int]) -> Dict[Tuple[int, str], Tuple[float, float]]:
        """
        Prepare a dictionary with values and coordinates for engraving.

        Parameters
        ----------
        x: float
            Start position in x-axis.
        y: float
            Start position in y-axis.
        width: float
            Width of burned squares.
        length: float
            Length of burned squares.
        space: float
            Space between burned squares.
        pwr_list: List[int]
            List with power values.
        speed_list: List[int]
            List with speed values.

        Returns
        -------
        sign_dict: Dict[Tuple[int, str], Tuple[float, float]]
            Dictionary with power/speed and their corresponding coordinates.
        """
        loc_y = y
        loc_x = x
        for pwr in pwr_list:
            loc_x += width + space
            self.sign_dict[(pwr, 'p')] = (loc_x, loc_y)

        loc_y = y  # Reset loc_y to y
        loc_x = x
        for speed in speed_list:
            loc_y += length + space  # Increment loc_y by length + space
            self.sign_dict[(speed, 's')] = (loc_x, loc_y)

        return self.sign_dict

    def pattern_start(self, x: float, y: float, width: float, length: float, space: float) -> Tuple[float, float]:
        """
        Calculate start position in X and Y axis.

        Parameters
        ----------
        x: float
            Start position in x-axis.
        y: float
            Start position in y-axis.
        width: float
            Width of burned squares.
        length: float
            Length of burned squares.
        space: float
            Space between burned squares.

        Returns
        -------
        x_start: float
            Start position in x-axis.
        y_start: float
            Start position in y-axis.
        """
        self.x_start = x + width + space
        self.y_start = y + length
        return self.x_start, self.y_start

    @staticmethod
    def mid_value(values_list: List[int]) -> int:
        """
        Find the middle value in the list.

        Parameters
        ----------
        values_list: List[int]
            List of values.

        Returns
        -------
        mid_value: int
            Middle values in the list.
        """
        middle = (len(values_list) - 1) // 2
        return values_list[middle]
