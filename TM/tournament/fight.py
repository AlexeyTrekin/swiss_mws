from enum import Enum
from .fighter import Fighter
from typing import List


class FightStatus(Enum):
    none = None

    planned = 'planned'
    going = 'going'
    paused = 'paused'
    finished = 'finished'

    # Here are the result statuses as well. Maybe enumerate them separately
    win = 'win'
    loss = 'loss'
    tech_win = 'tech_win'
    tech_loss = 'tech_loss'
    draw = 'draw'


class Round:

    def __init__(self, status=FightStatus.planned,
                 score_1: int = 0, score_2: int = 0,
                 doubles: int = 0, warnings_1: int = 0, warnings_2: int = 0,
                 current_time: int = 0, result_1=None, result_2=None):

        self.score_1 = score_1
        self.score_2 = score_2
        self.status = status if isinstance(status, FightStatus) else FightStatus(status)
        self.doubles = doubles
        self.warnings_1 = warnings_1
        self.warnings_2 = warnings_2
        self.current_time = current_time
        self.result_1 = result_1 if isinstance(result_1, FightStatus) else FightStatus(result_1)
        self.result_2 = result_2 if isinstance(result_2, FightStatus) else FightStatus(result_2)

    @property
    def to_dict(self):
        res = dict(self.__dict__)
        res['status'] = self.status.value
        res['result_1'] = self.result_1.value
        res['result_2'] = self.result_2.value
        return res


class Fight:

    def __init__(self, fighter_1: Fighter, fighter_2: Fighter,
                 status=FightStatus.planned,
                 rounds_num: int = 1, current_round: int = 0, rounds: List[Round] = None):

        self.fighter_1 = fighter_1
        self.fighter_2 = fighter_2
        self.status = status if isinstance(status, FightStatus) else FightStatus(status)
        self.rounds_num = rounds_num
        self.current_round = current_round
        if rounds is None:
            self.rounds = [Round() for _ in range(self.rounds_num)]
        else:
            self.rounds = rounds

    # === Properties that wrap around the self.rounds fields  ===
    @property
    def doubles(self):
        doubles = 0
        for r in self.rounds:
            doubles += r.doubles
        return doubles

    @property
    def warnings_1(self):
        warnings_1 = 0
        for r in self.rounds:
            warnings_1 += r.warnings_1
        return warnings_1

    @property
    def warnings_2(self):
        warnings_2 = 0
        for r in self.rounds:
            warnings_2 += r.warnings_2
        return warnings_2

    @property
    def total_score_1(self):
        total_score_1 = 0
        for r in self.rounds:
            total_score_1 += r.score_1
        return total_score_1

    @property
    def total_score_2(self):
        total_score_2 = 0
        for r in self.rounds:
            total_score_2 += r.score_2
        return total_score_2

    @property
    def round_score_1(self):
        # Not sure if it is okay to deduce it from the rounds, or should we have it explicitely
        round_score_1 = 0
        for r in self.rounds:
            if r.status == FightStatus.finished and r.result_1 == FightStatus.win:
                round_score_1 += 1
        return round_score_1

    @property
    def round_score_2(self):
        # Not sure if it is okay to deduce it from the rounds, or should we have it explicitely
        round_score_2 = 0
        for r in self.rounds:
            if r.status == FightStatus.finished and r.result_1 == FightStatus.win:
                round_score_2 += 1
        return round_score_2

    @property
    def result(self):
        raise NotImplementedError('The result calculation may be different depending on rules'
                                  'so it must be either implemented in inherited class'
                                  'or calculated outside of the Fight')
    # =========================================================

    @property
    def to_dict(self):
        """
        A wrapper to make the dict representation more useful
        Some of the values are substituted
        Initially it is a self.__dict__ to preserve everything else as is
        :return:
        """
        res = dict(self.__dict__)
        res['rounds'] = [r.to_dict for r in self.rounds]
        res['fighter_1'] = self.fighter_1.to_dict
        res['fighter_2'] = self.fighter_2.to_dict
        res['status'] = self.status.value
        res['doubles'] = self.doubles
        res['warnings_1'] = self.warnings_1
        res['warnings_2'] = self.warnings_2

        return res
