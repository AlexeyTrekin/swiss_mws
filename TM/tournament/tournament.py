import random
from .fighter import Fighter
from .fight import Fight
from typing import List


def find_fighters(pair: Fight, fighters: List[Fighter]):
    """
    Find the fighters in the list corresponding to the Fight
    :param pair:
    :param fighters:
    :return:
    """
    res = [None, None]
    for f in fighters:
        if f.fighter_id == pair.fighter_1:
            res[0] = f
        elif f.fighter_id == pair.fighter_2:
           res[1] = f
    return res


class Tournament:

    def __init__(self, pairing_function, fighters: List[Fighter] = None, start_rating=0, fight_cap=None):

        if fighters is not None:
            self.fighters = fighters
        else:
            self.fighters = []
        # fighters casted out of a tournament
        self.outs = []
        self.startRating = start_rating
        self.fightCap = fight_cap
        self.pairings = []
        self.pairing_function = pairing_function

    def make_pairs(self):
        # TODO: maker the pairings use the Fights
        self.pairings = self.pairing_function(self.fighters)

    def list_fighters(self):
        """
        :return: list of fighters in sorted order
        """
        return sorted(self.fighters, key=lambda f: f.rating, reverse=True)

    def update_fighters(self, fight: Fight):
        for fighter in find_fighters(fight, self.fighters):
            print(fighter)
            fighter.add_fight(fight)
            print(fighter)

    def read_fighters(self, filename: str, shuffle=False):
        raise NotImplementedError

    def write_standings(self, api, round_num):
        """

        :param api: API that complies with the format
        :param round_num: Number of the round to which we should write the standings
        :return:
        """
        raise NotImplementedError

    def write_pairs(self, api, round_num):
        """

        :param api: API that complies with the format
        :param round_num: Number of the round to which we should write the pairings
        :return:
        """
        # TODO: move Fight() construction to pairings
        fights = [Fight(pair[0].fighter_id, pair[1].fighter_id) for pair in self.pairings]
        fighters_dict = {}
        for f in self.fighters:
            fighters_dict[f.fighter_id] = f
        return api.write(fights, fighters_dict, round_num)

    def read_results(self, api, round_num):
        """

        :param api: API that complies with the format
        :param round_num:  Number of the round from which we should read the pairings results
        :return: list of fight results to apply to the fighters.
        Format: tuple of tuples ((fighter1, result1), (figther2, result2)), each is a string
        """
        # we parse and check the results before the tournament update in order to maintain sort of consistency
        fights = api.read(round_num)
        for fight in fights:
            self.update_fighters(fight)

    def remove(self, v=True):
        # TODO: maybe change to something more general? Or leave it to the Pairings?
        """
        moves the fighters with negative score out of the list
        One lucky can stand if there is need for the additional fighter to complete the even number
        :return:
        """
        new_outs = []
        minHP = self.fightCap

        for f in self.fighters:
            if f.rating <= 0:
                new_outs.append(f)
            else:
                minHP = min(minHP, f.rating)

        # If there 6 fighters or less, we can make finals:
        if len(self.fighters) - len(new_outs) <= 2:
            finalists = [f for f in self.fighters if f.rating > 0]
            candidates = [f for f in self.fighters if f.rating <= 0]
            if v:
                print("We need to setup an additional round to choose finalists.",
                      "Ready finalists are:")

                print(finalists)
                print('Candidates for additional round:')
                print(candidates)
            return finalists, candidates
        elif len(self.fighters) - len(new_outs) <= 6:
            finalists = [f for f in self.fighters if f.rating > 0]
            if v:
                print("We have the finalists:")
                print(finalists)
            return finalists, []
        # We leave one lucky fighter from the list if there is uneven number left
        elif (len(self.fighters) - len(new_outs)) % 2 != 0:
            lucky = random.choice(new_outs)
            if v:
                print('Lucky one: {}'.format(lucky))
            lucky.rating = minHP
            new_outs.remove(lucky)

        for f in new_outs:
            self.fighters.remove(f)
        self.outs += new_outs


