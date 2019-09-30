import random
from pathlib import Path
from fighter import Fighter, fighter_from_str
from typing import Tuple, List

def fight(f1: Fighter, f2: Fighter, result: Tuple[int, int]):
    """
    To put a record of a fight to the data
    :param f1:
    :param f2:
    :param result:
    :return:
    """
    f1.fight(f2, result[0])
    f2.fight(f1, result[1])

def hp(fighter: Fighter) -> int:
    # Function to sort fighters
    return fighter.hp


def alreadyPlayed(player1: Fighter, player2: Fighter) -> bool:
    """Have these two players already played in this tour?

        A boolean indicating if this would be a rematch
    """
    return player1.played(player2) > 0 or player2.played(player1) > 0


def decorate(filename):
    """
    We do not want to lose any of the data due to overwriting
    :param filename:
    :return:
    """
    if Path(filename).exists:
        noext = filename[:filename.rfind('.')]
        ext = filename[filename.rfind('.'):]
        decorated = filename
        i=1
        while Path(decorated).exists():
            decorated = noext + str(i) + ext
            i += 1
        return decorated
    else:
        return filename


class Tournament:

    def __init__(self, fighters: List[Fighter]=None, maxHP=12, fightCap=4):

        if fighters is not None:
            self.fighters = fighters
        else:
            self.fighters = []
        # fighters casted out of a tournament
        self.outs = []
        self.maxHP = maxHP
        self.fightCap = fightCap
        self.pairings = []

    def update_fighters(self, name1: str, name2: str, score: Tuple[int, int]):
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
        """

        :param result:
        :return:
        """
        try:
            sc1 = int(result[0][1])
            sc2 = int(result[1][1])
        except ValueError as e:
            print("Results of the fight must be integer!")
            raise e
        except IndexError as e:
            print("Results of the fight must be ((name1, res1),(name2, res2))!")
            raise e

            # Convert score to positive, because we only substract points in fights
        if sc1 < 0:
            sc1 *= -1
        if sc2 < 0:
            sc2 *= -1
        if sc1 > self.fightCap or sc2 > self.fightCap:
            raise ValueError("Results must be not greater than {}".format(self.fightCap))

        return result[0][0], result[1][0], (sc1, sc2)

    def read_fighters(self, filename: str):
        with open(filename) as src:
            self.fighters = [fighter_from_str(s, self.maxHP) for s in src.readlines()]

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
        results = [self.parse_result(res) for res in api.read(round_num)]
        for res in results:
            self.update_fighters(*res)

    def swissPairings(self):
        """Returns a list of pairs of players for the next round of a match in this tour.

        Assuming that there are an even number of players registered, each player
        appears exactly once in the pairings.  Each player is paired with another
        player with an equal or nearly-equal HP, that is, a player adjacent
        to him or her in the standings.  Rematches are not allowed, so all pairings are new
        (excluding situations when all pairs have matched, see Fighter.normalize_played )

        Returns: a list of tuples of fighters
        """

        if len(self.fighters) % 2 != 0 or len(self.fighters) == 0:
            raise ValueError("Number of fighters is {}, does not suit for pairing".format(len(self.fighters)))

        standings = sorted(self.fighters, key=hp)

        pairings = []

        for i in range(0, len(standings), 2):
            for j in range(i + 1, len(standings)):
                if not alreadyPlayed(standings[i], standings[j]):
                    # good pair found, swap into place then break the inner loop
                    while j > i + 1:
                        standings[j - 1], standings[j] = standings[j], standings[j - 1]
                        j -= 1
                    break
            pairings.append((standings[i], standings[i + 1]))
        self.pairings = pairings

    def remove(self):
        """
        moves the fighters with negative score out of the list
        One lucky can stand if there is need for the additional fighter to complete the even number
        :return:
        """
        new_outs = []
        minHP = self.fightCap

        for f in self.fighters:
            if f.hp <= 0:
                new_outs.append(f)
            else:
                minHP = min(minHP, f.hp)

        # If there 6 fighters or less, we can make finals:
        if len(self.fighters) - len(new_outs) <= 2:
            print("We need to setup an additional round to choose finalists.",
                  "Ready finalists are:")
            print([f for f in self.fighters if f.hp > 0])
            print('Candidates for additional round:')
            print([f for f in self.fighters if f.hp <= 0])
            return
        elif len(self.fighters) - len(new_outs) <= 6:
            print("We have the finalists:")
            print([f for f in self.fighters if f.hp > 0])
        # We leave one lucky fighter from the list if there is uneven number left
        elif (len(self.fighters) - len(new_outs)) % 2 != 0:
            lucky = random.choice(new_outs)
            print('Lucky one: {}'.format(lucky))
            lucky.hp = minHP
            new_outs.remove(lucky)

        for f in new_outs:
            self.fighters.remove(f)
        self.outs += new_outs

