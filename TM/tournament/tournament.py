import random
from .fighter import Fighter
from .fight import Fight, Round, FightStatus
from typing import Tuple, List


def fight(fighter_1: Fighter, fighter_2: Fighter, result: Tuple[int, int]):
    """
    To put a record of a fight to the data
    It is a legacy function that is used with the
    :param fighter_1:
    :param fighter_2:
    :param result:
    :return:
    """
    # a proxy fight from the given results. In the future, the fight will come as a dict from the API
    r = Round(status=FightStatus.finished, score_1=result[0], score_2=result[1])
    f = Fight(fighter_1.fighter_id, fighter_2.fighter_id, status=FightStatus.finished, rounds=[r])

    # here we insert the tournament rules that state that the rating score is the total score.
    # we need this to be a slot for a function that returns rating delta from the Fight
    # TODO: move this out of tournament class and insert this functinonality either in executable or from config
    f.rating_score_1 = f.total_score_1
    f.rating_score_2 = f.total_score_2

    fighter_1.add_fight(f)
    fighter_2.add_fight(f)


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

    def update_fighters(self, name1: str, name2: str, score: Tuple[int, int]):
        # TODO: change score to Fight
        """
        :param name1: unique name of the first fighter
        :param name2: unique name of the second fighter
        :param score: difference in score. If negative, HP will diminish, if positive - increase.
        :return:
        """
        f1 = None
        f2 = None

        for f in self.fighters:
            if f.name == name1:
                f1 = f
            elif f.name == name2:
                f2 = f
        if f1 is None or f2 is None:
            raise ValueError("One of the fighters named {}, {} not found".format(name1, name2))
        fight(f1, f2, score)

    def parse_result(self, result):
        #  This is a MWS tournament legacy.
        #  It will be deprecated and functionality will be moved to the inherited class MWS_tournament, if needed
        """

        :param result:
        :return:
        """
        try:
            # results must be negative regardless of input. We know that there is no positive score in MWS,
            # so we make the operators work easier with this hack. They can either put or miss '-' sign without problems
            sc1 = -abs(int(result[0][1]))
            sc2 = -abs(int(result[1][1]))
        except ValueError as e:
            print("Results of the fight must be integer!")
            raise e
        except IndexError as e:
            print("Results of the fight must be ((name1, res1),(name2, res2))!")
            raise e
        # FightCap is positive, because reasons/
        if abs(sc1) > self.fightCap or abs(sc2) > self.fightCap:
            raise ValueError("Results must be not greater than {}".format(self.fightCap))

        return result[0][0], result[1][0], (sc1, sc2)

    def read_fighters(self, filename: str, shuffle=False):
        with open(filename) as src:
            self.fighters = [Fighter.from_str(s, self.startRating) for s in src.readlines()]
            if shuffle:
                random.shuffle(self.fighters)

    def write_standings(self, api, round_num):
        """

        :param api: API that complies with the format
        :param round_num: Number of the round to which we should write the standings
        :return:
        """
        api.write(self.fighters, round_num)

    def write_pairs(self, api, round_num):
        """

        :param api: API that complies with the format
        :param round_num: Number of the round to which we should write the pairings
        :return:
        """
        return api.write(self.pairings, round_num)

    def read_results(self, api, round_num):
        """

        :param api: API that complies with the format
        :param round_num:  Number of the round from which we should read the pairings results
        :return: list of fight results to apply to the fighters.
        Format: tuple of tuples ((fighter1, result1), (figther2, result2)), each is a string
        """

        # we parse and check the results before the tournament update in order to maintain sort of consistency
        data = api.read(round_num)
        results = [self.parse_result(res) for res in data]
        for res in results:
            self.update_fighters(*res)

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


