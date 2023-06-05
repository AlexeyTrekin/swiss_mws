from uuid import UUID, uuid4

from pydantic import BaseModel, Field
from typing import List
from status import Status
from .fighter import Fighter
from .stage import TournamentStage


class Tournament(BaseModel):
    """
    In the Tournament class we:
     - store all the tournament data, such as Fighters, and Fights statistics and so on.
     - connect all the parts of the system (pairings, API, fighters)
     - provide interfaces for the executable

     The Tournament is bound to a single fighters list and the pairing function,
     so it describes actually a stage in the tournament. If we want to make the finals, we create a new Tournament

    """
    id: UUID = Field(default_factory=uuid4)
    status: Status = Status.none
    fighters: List[Fighter] = Field(default_factory=list)
    stages: List[TournamentStage] = Field(default_factory=list)

