from random import randint
from TM.tournament import Tournament, Fighter, TournamentRules
from TM.pairings import swiss_pairings, swiss_pairings_old

# Tournament size varaints
MIN_FIGHTERS = 8
MAX_FIGHTERS = 50
#Default (maximum) hp of a fighter
MAX_HP = 20
# Fight cap - maximum lost HP in a fight
CAP = 5


class ProxyApi:
    def __init__(self, cap):
        self.all_fights = []
        self.cap = cap
        self.pairs = []

    def write(self, pairs, round_num):
        self.pairs = [(p[0].name, p[1].name) for p in pairs]

    def read(self, round_num):
        """
        Generates a random results, where one of the pair receives -cap, and the other a random number from -cap-1 to 0

        :param round_num: Not used here, inherited from interface
        :return: results as a list of tuples (fighter1, points1, fighter2, points2)
        """
        results = []
        for pair in self.pairs:
            res = [-self.cap, randint(-self.cap, 0)]
            if randint(0, 1) == 0:
                res = [res[1], res[0]]
            results.append(((pair[0], res[0]), (pair[1], res[1])))
        self.all_fights.append(results)
        return results


def conduct_tournament(pairing_function, fighters_num, hp, cap):
    rules = TournamentRules(fight_cap=cap, pairing_function=pairing_function, start_rating=hp)
    fighters = [Fighter(fighter_id=str(i), last_name='', first_name=str(i), rating=hp) for i in range(fighters_num)]
    tour = Tournament(fighters=fighters, rules=rules)
    api = ProxyApi(cap=cap)

    r = 0
    while tour.remove(v=False) is None:
        tour.make_pairs()

        # test no repeated fights - the only thing we really need here
        for p in tour.pairings:
            if p[1].name in p[0].enemies or p[0].name in p[1].enemies:
                return False

        tour.write_pairs(api, r)
        tour.read_results(api, r)
        r += 1
    return True


def test_tournament_passes_without_repeats():
    attempts = 100

    for fighters_num in range(MIN_FIGHTERS, MAX_FIGHTERS, 4):
        fails = 0
        for run in range(attempts):
            if not conduct_tournament(pairing_function=swiss_pairings, fighters_num=fighters_num, hp=MAX_HP, cap=CAP):
                fails += 1
        # We assume 3% probability of fail (repeated pairing) a normal chance
        assert fails <= 3
        print(f'{fails} of {attempts} failed for {fighters_num} fighters')
