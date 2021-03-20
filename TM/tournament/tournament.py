import json
import warnings

from typing import List, Tuple
from .fighter import Fighter
from .fight import Fight, FightStatus


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


class TournamentRules:
    """
    This class describes the rules of a tournament, and contains every parameter we can imagine.
     If a parameter is missing, we should add it to this class.
     The rules can be configured from a file and exported as json for the

    """

    def __init__(self, pairing_function, sorting_function=None, rating_fn=None,
                 start_rating=0,
                 max_rating=None, min_rating=None,
                 round_excess_cap=None, round_points_cap=None,
                 warnings_per_fight=None, warnings_total=None, doubles_cap=None,
                 time=None, last_exchange_time=None, last_exchange_start=None, sudden_death_time=None,
                 rounds_num=1, preserve_score=False):
        # A function for the pairs selection. Swiss, round, group etc.
        self.pairing_function = pairing_function
        # A function for sorting the fighters for ranking.
        # It is not used in pairings (where rating is enough) but can be used for the final rankings,
        # and take into account additional coefficients
        self.sorting_fn = sorting_function
        # a function that calculates rating score from the fight rounds
        self.rating_fn = rating_fn
        # Rating with which a fighter starts. Is zero in most cases
        self.start_rating = start_rating
        # max rating points per fight
        self.max_rating = max_rating
        # min rating point per fight
        self.min_rating = min_rating

        # max points difference, which stops the round
        self.round_excess_cap = round_excess_cap
        # max points per round
        self.round_points_cap=round_points_cap

        self.rounds_num = rounds_num
        #Maximum doubles, which stops the fight
        self.doubles_cap = doubles_cap
        #time per round
        self.time = time
        # Time for the last exchange
        self.last_exchange_time = last_exchange_time
        # Time in the round when the last exhange starts
        self.last_exchange_start = last_exchange_start
        self.sudden_death_time = sudden_death_time
        #
        self.warnings_per_fight = warnings_per_fight
        self.warnings_total = warnings_total
        # If True, the score between rounds is kept, if False, each new round starts from 0=0.
        self.preserve_score = preserve_score
        # More parameters

    @property
    def to_dict(self):
        # todo: change to comply with API format
        return dict(self.__dict__)

    @property
    def json(self):
        return json.dumps(self.to_dict)


class Tournament:
    """
    In the Tournament class we:
     - store all the tournament data, such as Fighters, and Fights statistics and so on.
     - connect all the parts of the system (pairings, API, fighters)
     - provide interfaces for the executable

     The Tournament is bound to a single fighters list and the pairing function,
     so it describes actually a stage in the tournament. If we want to make the finals, we create a new Tournament

    """

    def __init__(self, rules: TournamentRules,
                 fighters: List[Fighter] = None):

        self.rules = rules

        if fighters is not None:
            self.fighters = fighters
        else:
            self.fighters = []

        # fighters casted out of a tournament
        self.pairings = []

    def add_fighter(self, new_fighter: Fighter):
        """
        Adds a fighter to the current tournament. For now we do not check if this tournament will be valid after the addition.
        It can be ruined with some collisions and so on, so this function should be used with caution.
        Maybe, later we should implement the check if the tournament allows the fihgter addition/deletion

        If the fighter with this ID is already in the tournament, the function does nothing but raise a warning
        :param new_fighter: Fighter to be added to the tournament.
        :return:
        """
        if new_fighter in self.fighters:
            warnings.warn(f'The fighter {new_fighter.fighter_id}, {new_fighter.name} is already enlisted')
            return
        self.fighters.append(new_fighter)

    def remove_fighter(self, fighter):
        """
        Remover a fighter from the current tournament. For now we do not check if this tournament will be valid after the removal.
        It can be ruined with some collisions and so on, so this function should be used with caution.
        Maybe, later we should implement the check if the tournament allows the fihgter addition/deletion

        If the fighter with this ID is not in the tournament, the function does nothing but raise a warning
        :param fighter: Fighter to be removed to the tournament.
        :return:
        """
        if fighter not in self.fighters:
            warnings.warn(f'The fighter {fighter.fighter_id}, {fighter.name} is not in the tournament')
            return
        self.fighters.remove(fighter)

    def update_fighters(self, fight: Fight):
        """
        Finds and updates both fighters affected by the Fight
        :param fight: Fight object. Should have status='finished'
        :return:
        """
        for fighter in find_fighters(fight, self.fighters):
            fighter.add_fight(fight)

    def read_fighters(self, filename: str, shuffle=False):
        raise NotImplementedError

    @property
    def config(self):
        return self.config

    def list_fighters(self):
        """
        Lists the fighters in a sorted order; by default the sorting function is Fighter.rating,
        but it can be overridden in the TournamentRules

        :return: list of fighters in sorted order
        """
        if self.rules.sorting_fn is not None:
            return sorted(self.fighters, key=self.rules.sorting_fn, reverse=True)
        return sorted(self.fighters, key=lambda f: f.rating, reverse=True)

    def write_standings(self, api, round_num):
        """
        Writes the standings ( A sorted by rating list of Fighters ) to the outer interface
        :param api: API that complies with the format
        :param round_num: Number of the round to which we should write the standings
        :return:
        """
        raise NotImplementedError

    def make_fight(self, pair: Tuple[Fighter, Fighter]) -> Fight:
        """
        Makes a default (planned) fight from a pair of the fighters in compliance with the tournament rules.
        Maybe, in the future the construction will become more complex
        :return:
        """
        # Incorporate the starting score into the planned Fight
        f = Fight(pair[0].fighter_id, pair[1].fighter_id,
                  rounds_num=self.rules.rounds_num)
        return f

    def check_fight(self, fight: Fight):
        """
        Checks if the fight complies to the current tournament rules and can be applied
        :param fight:
        :return:
        """
        # we do not apply unfinished fights, yes?
        if fight.status != FightStatus.finished:
            return False

        # We need the rating score, and will calculate it if the rules allow us to:
        if self.rules.rating_fn is not None:
            fight.count_rating_points(self.rules.rating_fn)

        # rounds num
        if len(fight.rounds) > self.rules.rounds_num:
            return False

        # rating points cap
        if self.rules.max_rating is not None \
                and (fight.rating_score_1 > self.rules.max_rating or fight.rating_score_2 > self.rules.max_rating):
            return False
        if self.rules.min_rating is not None \
                and (fight.rating_score_1 < self.rules.min_rating or fight.rating_score_2 < self.rules.min_rating):
            return False

        # points and excess cap in a round - not present in rules yet
        for r in fight.rounds:
            if self.rules.round_points_cap \
                    and (r.score_1 > self.rules.round_points_cap or r.score_2 > self.rules.round_points_cap):
                return False
            if self.rules.round_excess_cap \
                    and abs(r.score_1 - r.score_2) > self.rules.round_excess_cap:
                return False

        # doubles cap
        if self.rules.doubles_cap \
                and fight.doubles > self.rules.doubles_cap:
            return False

        # warnings cap
        if self.rules.warnings_per_fight \
                and (fight.warnings_1 > self.rules.warnings_per_fight
                     or fight.warnings_2 > self.rules.warnings_per_fight):
            return False
        return True

        # Draw when it is not allowed

    def make_pairs(self):
        """
        Invokes the pairing functions and makes new pairs.
        The pairs are made after the current state of the Fighters; the previous rounds pairings are not stored.
        Maybe we should archive it somehow, but now it is saved only via API
        :return:
        """
        self.pairings = [self.make_fight(pair) for pair in self.pairing_function(self.fighters)]

    def write_pairs(self, api, round_num):
        """
        Writes the generated pairs for the selected round to the outer interface
        :param api: API that complies with the format
        :param round_num: Number of the round to which we should write the pairings
        :return:
        """

        fighters_dict = {}
        for f in self.fighters:
            fighters_dict[f.fighter_id] = f
        return api.write(self.pairings, fighters_dict, round_num)

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
            if not self.check_fight(fight):
                # It works now with mws.py but maybe we need a better error handling way.
                raise ValueError(f'One of the results do not meet the tournament rules: {fight.to_dict}')
        for fight in fights:
            self.update_fighters(fight)

    def finalize(self, finalists_num=None):
        """
        Makes the list of the finalists, and if the rating is equal for a part of them,
        the additional tie-break fights are planned as self.pairings
        :param finalists_num: number of finalists to create.
        :return: finalists and candidates (the ones who have equal rating and should go to the additional fights)
        """
        standings = self.list_fighters()
        # if the fighters on the boundary of finalists' list have not the same rating, which means that it
        boundary = self.rules.sorting_fn(standings[finalists_num-1])
        if boundary > self.rules.sorting_fn(standings[finalists_num]):
            return standings[:finalists_num], []
        else:
            # By now, it is unclear how to manage tie-breaks and not disturb the rating:
            # if we simply give the rating to the fencers, they can overcome the higher ranked fencers.
            # if we do not give it - then how?
            # Maybe a separate Tournament with tie-breaks?
            # Now the procedure is outside the Tournament.
            candidates = [f for f in standings if self.rules.sorting_fn(f) == boundary]
            ready_finalists = [f for f in standings if self.rules.sorting_fn(f) >= boundary]

            #self.pairings = TieBreakPairings(slots=finalists_num - ready_finalists)(candidates)
            return ready_finalists, candidates


### ==================== HERE STARTS THE LEGACY =================== ###

    # These properties were previously the class members, now moved to the rules. Will be deprecated.
    @property
    def pairing_function(self):
        return self.rules.pairing_function

    @property
    def startRating(self):
        return self.rules.start_rating

    @property
    def fightCap(self):
        return self.rules.max_rating