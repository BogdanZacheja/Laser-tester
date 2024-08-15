import numpy as np
from typing import List


class Divider:
    """
    Class for creating a list of values between two parameters.
    """

    def __init__(self):
        self.values_list = []

    def values(self, start: int, end: int, steps: int) -> List[int]:
        """
        Method to divide the range between start and end parameters
        into equal pieces and create a list of values.

        Parameters
        ----------
        start: int
            Start of the range.
        end: int
            End of the range.
        steps: int
            Number of pieces to divide the range.

        Returns
        -------
        values_list: List[int]
            List of values in the given range.
        """
        self.values_list = list(np.linspace(start, end, steps, dtype=int))
        return self.values_list

    @staticmethod
    def find_longest(lst: List[int]) -> int:
        """
        Method to find the number of digits in the longest value in the list.

        Parameters
        ----------
        lst: List[int]
            List of values.

        Returns
        -------
        longest: int
            Number of digits in the longest value in the list.
        """
        longest = max(lst)
        return len(str(longest))

    @staticmethod
    def mid_value(lst: List[int]) -> int:
        """
        Method to find the middle value in the list.

        Parameters
        ----------
        lst: List[int]
            List of values.

        Returns
        -------
        mid_value: int
            Middle values in the list.
        """
        mid = len(lst) // 2
        mid_value = lst[mid]
        return mid_value
