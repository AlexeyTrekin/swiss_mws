from pydantic import BaseModel
from typing import List
from .stage_json import CreateStageInput
from .fighter_json import CreateFighterInput


class CreateTournamentInput(BaseModel):
    fighters: List[CreateFighterInput]
    stages: List[CreateStageInput]

