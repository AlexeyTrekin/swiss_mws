from enum import Enum
from typing import List
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class PairingFunction(str, Enum):
    round = 'round'
    group = 'group'
    playoff = 'playoff'
    swiss = 'swiss'


class RatingFunction(str, Enum):
    pass


class FightRules(BaseModel):
    """
    Rules that apply to a particular fight
    They must be known to secretary's app
    """
    preserve_round_score: bool
    sudden_death: bool
    time_is_clean: bool

    rounds_num: int
    round_time_cap: int
    sudden_death_time: int = 0
    round_points_cap: int

    warnings_cap: int
    doubles_cap: int


class PairingRules(BaseModel):
    """ Rules that apply to matching pairs of the fighters """
    # Function that calculates fighters pairings based on the fighters list with rating
    pairing_fn: PairingFunction


class GeneralRules(BaseModel):
    """ General tournament (stage) rules that are checked through the whole tournament"""
    warnings_cap: int
    # Functions that calculates fighter's rating score based on the fight result
    rating_functions: List[RatingFunction]


class TournamentRules(BaseModel):
    """
    This class describes the rules of a tournament, and contains every parameter we can imagine.
     If a parameter is missing, we should add it to this class.
     The rules can be configured from a file and exported as json for the

    """
    id: UUID = Field(default_factory=uuid4)
    fight_rules: FightRules
    pairing_rules: PairingRules
    general_rules: GeneralRules


