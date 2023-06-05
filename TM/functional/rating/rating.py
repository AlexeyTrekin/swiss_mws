from typing import Tuple

from ...model import Fight


class Rating(list):
    """
    Rating is a list of numbers, which is compared one-by-one.
    This means that rating can contain a number of coefficients, each next less significant than the previous
    """
    def __init__(self):
        pass

    def __eq__(self, other):
        return

    def __gt__(self, other):
        return

    def __lt__(self, other):
        return


class RatingCalc:
    """
    Base class for rating calculation:
    """

    def __call__(self, fight: Fight) -> Tuple[int, int]:
        """
        Returns the fight rating based on the fight result
        """
        raise NotImplementedError
