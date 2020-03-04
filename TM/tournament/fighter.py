from enum import Enum
from typing import Optional, List
from collections import defaultdict

from .fight import Fight, Round

class Division(Enum):
    base = 'base'
    pl = 'pl'
    tc = 'tc'


class Fighter:

    def __init__(self, fighter_id: str, first_name: str, last_name: str,
                 club: str = '', city: str = '', country: str = '',
                 rating: int = 0, global_rating: int = 0, division: Division = Division.base,
                 warnings: int = 0, doubles: int = 0, fights: Optional[List[Fight]] = None):
        """

        :param fighter_id: UNIQUE fighter identifier
        :param first_name: personal name
        :param last_name: family name
        :param club:
        :param city:
        :param country:
        :param rating: tournament rating of the fighter
        :param global_rating: Rating outside of the tournament, maybe from hfdb or hemaratings
        :param division: FDF fighter division
        :param warnings: number of warnings in current tournament
        :param doubles: number of doubles in current tournament
        :param fights: list of fights conducted by this fighter in current tournament
        """

        self.fighter_id = fighter_id
        self.first_name = first_name
        self.last_name = last_name
        self.club = club
        self.city = city
        self.country = country
        self.rating = rating
        self.global_rating = global_rating
        self.division = division if isinstance(division, Division) else Division(division)
        self.warnings = warnings
        self.doubles = doubles

        if fights is None:
            self.fights = []
        else:
            self.fights = fights

    @property
    def enemies(self):
        """
        The property (Legacy) that reports which fighters have this one had fights with
        :return:
        dict: key=fighter_id, value = number of fights between them
        """
        enemies = defaultdict(int)
        for f in self.fights:
            # Should we add correctness check? Probably no, as the function may be deprecated soon
            if f.fighter_1 != self.fighter_id:
                enemies[f.fighter_1] += 1
            else:
                enemies[f.fighter_2] += 1
        return enemies

    @property
    def name(self):
        return self.last_name + ' ' + self.first_name

    @property
    def to_dict(self):
        """
        A wrapper to make the dict representation more useful
        Some of the values are substituted
        :return:
        """
        res = dict(self.__dict__)
        res['division'] = self.division.value
        return res

    def __repr__(self):
        return self.name + ', ' + str(self.rating)

    def to_list(self):
        """
        Legacy - for google api
        :return:
        """
        return [self.name, str(self.rating), '']

    def add_fight(self, fight):
        """
        Legacy - for current tournament's fight().
        It constructs a new one-Round Fight object
        :param other:
        :param hp_lost:
        :return:
        """
        if fight.fighter_1 == self.fighter_id:
            self.rating += fight.rating_score_1
        elif fight.fighter_2 == self.fighter_id:
            self.rating += fight.rating_score_2
        else:
            raise ValueError(f'Fighter {self.fighter_id} is not in the fight that is added')
        self.fights.append(fight)

    def played(self, other):
        """
        Legacy. Will be replaced by self.fights and its queries
        :param other:
        :return:
        """
        if other.name in self.enemies.keys():
            return self.enemies[other.name]
        else:
            return 0

    def normalize_played(self, others):
        """
        Not used now. Probably not necessary for new swiss system

        If all others have played at least once, we cannot make pairings any more, as the system tries to
        avoid repetitive figths. So, if all the 'played' vaules for current opponents are positive,
        we substract from it to have zeros again
        This can be not mutual, as there may be free slots for one of the fighters and no slots for the other one.
        That is why we must check played() for both
        :param others: list of Fighters to match
        :return: None
        """
        # TODO: test if there are problems without it and remove if not
        min_played = 99

        for o in others:
            if o.name not in self.enemies.keys():
                return
            else:
                m = min(min_played, self.enemies[o.name])
        if min_played == 0:
            return
        # If we reached here it means that all others played at least 1 time
        # Then we substract 1 from all of them to nullify at least one of them
        print(self.name + " played with all at least {} times".format(m))
        for o in others:
            self.enemies[o.name] -= m
