from typing import List
from uuid import UUID, uuid4

from pydantic import BaseModel, Field
from .status import Status
from .fight import Fight
from .ruleset import TournamentRules


class TournamentStage(BaseModel):
    """
    Tournament stage is a part of the tournament with fixed ruleset
    The tournament can contain several stages with diffferent rulesets (pools + playoff + finals)
    """
    tournament_id: UUID
    id: UUID = Field(default_factory=uuid4)
    ruleset: TournamentRules
    fights: List[Fight]
    status: Status = Status.none
