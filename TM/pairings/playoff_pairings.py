from typing import List
from TM.tournament import Fighter
from .pairings import Pairings
import copy


class PlayoffPairings(Pairings):

    def __init__(self, initial_standings=None):
        super().__init__()
        self.prev_round_standings = copy.deepcopy(initial_standings)
        if self.prev_round_standings is not None:
            # Stand them by the rating for further pairing
            self.prev_round_standings.sort(key=lambda x: x.rating, reverse=True)
        self.round = 1

    def __call__(self, fighters):
        """
        Make pairings for every pair in 'fighters', arranging it so that none will have 2 fights in a row
        (except case with 3 or 4 fighters)
        :param fighters: list of fighters
        :return: list of Fights (tuples)
        """
        # Special cases
        if self.prev_round_standings is None:
            pairs =  self._playoff_rating_pairings(fighters)
        else:
            pairs = self._playoff_predefined_pairings(fighters)
        self.round += 1
        return pairs

    def _playoff_predefined_pairings(self, fighters: List[Fighter]):
        """

        :param fighters:
        :return:
        """
        fighters_num = len(fighters)
        if fighters_num % 2 != 0 or fighters_num <= 0:
            raise ValueError('There must be even number of fighters for playoff')

        # it is either all the fighters that were in the prev stage or half of them
        if len(self.prev_round_standings) != len(fighters) and len(self.prev_round_standings) != 2*len(fighters):
            raise ValueError(f'Number of fighters at the current stage is {len(fighters)}'
                             f' which does not correspond to {len(self.prev_round_standings)} fighters at the previous round')

        if self.round > 1:
            # this means that it is not the first round
            # Find the previous round standings and assign the fighters the correct rating
            # That is max (self.rating, opponent.rating)

            for fighter in fighters:
                prev_round_index = self.prev_round_standings.index(fighter)
                prev_round_opponent = self.prev_round_standings[len(self.prev_round_standings) - prev_round_index - 1]

                fighter.rating = max(fighter.rating, prev_round_opponent.rating)

        #elif len(self.prev_round_standings) == 4:
        #    # Four fighters come to final and 3rd place fight
        #    standings = sorted(fighters, key=lambda x: x.rating, reverse=True)
        #    pairings = [(standings[0], standings[1]),(standings[2], standings[3])]
        #    return pairings
        # else - it is the correct first round and no corrections should be made to the rating

        pairings = []
        standings = sorted(fighters, key=lambda x: x.rating, reverse=True)
        self.prev_round_standings = copy.deepcopy(standings)

        for i in range(fighters_num // 2):
            pairings.append((standings[i], standings[fighters_num - i - 1]))
        return pairings

    @staticmethod
    def _playoff_rating_pairings(fighters: List[Fighter]):
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

