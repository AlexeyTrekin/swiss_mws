from typing import List, Tuple
from TM.tournament import Fighter


class Pairings:
    """
    Just an abstract class that describes the pairings interface.
    Pairings is a callable that takes list of Fighters and returns all the pairs due to the pairing rules

    The pairs are just a tuples of two Fighters, because the way that Fight is established depends on the TournamentRules,
    and the pairings do not need to know everything about them
    """

    def __init__(self):
        pass

    def __call__(self, fighters: List[Fighter]) -> List[Tuple[Fighter, Fighter]]:
        raise NotImplementedError
