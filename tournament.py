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

    def __init__(self, fighters: List[Fighter]=None, maxHP=12, fightCap=3):

        if fighters is not None:
            self.fighters = fighters
        else:
            self.fighters = []
        # fighters casted out of a tournament
        self.outs = []
        self.maxHP = maxHP
        self.fightCap = fightCap
        self.pairings = []

    def update_fighters(self, name1: str, name2:str, score: Tuple[int, int]):
        """
        :param f1: unique name of the first fighter
        :param f2: unique name of the second fighter
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

    def read_fighters(self, filename: str):
        with open(filename) as src:
            self.fighters = [fighter_from_str(s, self.maxHP) for s in src.readlines()]

    def standings_to_txt(self, filename: str):
        with open(decorate(filename), 'w') as dst:
            for f in self.fighters:
                dst.write(f.to_str() + '\n')

    def all_to_txt(self, filename: str):
        with open(decorate(filename), 'w') as dst:
            for f in self.fighters:
                dst.write(f.to_str() + '\n')
        for f in self.outs:
            dst.write(f.to_str() + '\n')

    def standings_to_csv(self, filename):
        """
        Writes fighters list for display as a table in format "name, HP", sorted by HP.
        :param filename:
        :return:
        """
        with open(decorate(filename), 'w') as dst:
            for f in sorted(self.fighters, key=hp):
                dst.write(repr(f) + '\n')

    def pairs_to_csv(self, filename):
        """
        Writes fights (pairs) list for display as a table in format "name1, , , name2"
        :param filename:
        :return:
        """
        with open(decorate(filename), 'w') as dst:
            dst.write('RED, Red HP, Red score, Blue score, Blue HP, BLUE\n')
            for p in self.pairings:
                dst.write(p[0].name + ',' + str(p[0].hp) +  ', , , ' + str(p[1].hp) + ',' + p[1].name + '\n')

    def results_from_csv(self, filename):
        with open(filename) as src:
            for p in src.readlines()[1:]:
                split = p.split(',')
                self.update_fighters(split[0].rstrip().strip('\"'), split[5].rstrip().strip('\"'),
                                     (int(split[2].rstrip().strip('\"')), int(split[3].rstrip().strip('\"'))))

    def swissPairings(self):
        """Returns a list of pairs of players for the next round of a match in this tour.

        Assuming that there are an even number of players registered, each player
        appears exactly once in the pairings.  Each player is paired with another
        player with an equal or nearly-equal HP, that is, a player adjacent
        to him or her in the standings.  Rematches are not allowed, so all pairings are new
        (excluding situations when all pairs have matched, see Fighter.normalize_played )

        Returns: a list of tuples of fighters
        """

        if len(self.fighters) %2 != 0 or len(self.fighters) == 0:
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
            print([f for f in self.fighters if f.hp < 0])
            return
        elif len(self.fighters) - len(new_outs) <= 6:
            print("We have the finalists:")
            print([f for f in self.fighters if f.hp > 0])
            return
        # We leave one lucky fighter from the list if there is uneven number left
        elif (len(self.fighters) - len(new_outs)) % 2 != 0:
            lucky = random.choice(new_outs)
            print('Lucky one: {}'.format(lucky))
            lucky.hp = minHP
            new_outs.remove(lucky)

        for f in new_outs:
            self.fighters.remove(f)
        self.outs += new_outs

