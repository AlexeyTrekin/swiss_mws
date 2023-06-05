from enum import Enum
from pydantic import BaseModel


class Status(str, Enum):
    """Status can be used for any event"""
    none = "NONE"
    planned = 'PLANNED'
    going = 'GOING'
    paused = 'PAUSED'
    finished = 'FINISHED'
    canceled = 'CANCELLED'


class RoundStatus(Status):
    pass


class FightStatus(Status):
    pass


class Result(str, Enum):
    """
    result for a particular fighter in a fight/round
    """
    none = "NONE"
    win = 'WIN'
    loss = 'LOSS'
    tech_win = 'TECH_WIN'
    tech_loss = 'TECH_LOSS'
    draw = 'DRAW'
