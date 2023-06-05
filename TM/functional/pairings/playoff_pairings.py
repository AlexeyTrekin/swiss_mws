from typing import List
from .pairings import Pairings
from ...model import Fighter


class PlayoffPairings(Pairings):
    def __call__(self, fighters: List[Fighter]):
        """
        This function applies to every round of the playoff tournament, and
         it does not know how the tournament scheme is organized.
         So the rating results must be updated every round.

        To make a correct 'snake-like' pairing it should be done as follows:
        - in first round, every fighter gets the rating that led to their position, (the more the rating - the higher position)
        - in every following round, the winner of the fight gets max(self.rating, opponent.rating).

        After a group selection scheme, the playoff scheme can differ to avoid same-group pairs.


        Pairs always the highest rated fighter with the lowest rated. While it may be OK for the first playoff round,
        we need something more advanced to implement the 'snake-like' playoff
        :param fighters:
        :return:
        """
        fighters_num = len(fighters)
        if fighters_num % 2 != 0 or fighters_num <= 0:
            raise ValueError('There must be even number of fighters for playoff')

        pairings = []
        standings = sorted(fighters, key=get_rating, reverse=True)

        for i in range(fighters_num//2):
            pairings.append((standings[i], standings[fighters_num - i - 1]))
        return pairings