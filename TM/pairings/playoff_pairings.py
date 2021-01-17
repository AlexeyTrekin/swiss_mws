from typing import List
from TM.tournament import Fighter
from .pairings import Pairings

class PlayoffPairings(Pairings):

    def __call__(self, fighters):
        """
        Make pairings for every pair in 'fighters', arranging it so that none will have 2 fights in a row
        (except case with 3 or 4 fighters)
        :param fighters: list of fighters
        :return: list of Fights (tuples)
        """
        # Special cases
        return playoff_rating_pairings(fighters)


def dumb_playoff_pairings(fighters):
    """
    Just makes pairs in order 1-2, 3-4, ...
    :param fighters:
    :return:
    """
    if len(fighters) % 2 != 0 or len(fighters) == 0:
        raise ValueError('There must be even number of fighters for playoff')

    pairings = []
    for i in range(len(fighters)//2):
        pairings.append((fighters[i*2], fighters[i*2 + 1]))
    return pairings


def playoff_rating_pairings(fighters: List[Fighter]):
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
    standings = sorted(fighters, key=lambda x:x.rating, reverse=True)

    for i in range(fighters_num//2):
        pairings.append((standings[i], standings[fighters_num - i - 1]))
    return pairings