from uuid import UUID
from typing import Optional
from pydantic import BaseModel


class CreateStageInput(BaseModel):
    tournament_id: Optional[UUID] = None
    ruleset_id: Optional[UUID] = None
    ruleset: Optional[CreateRulesetInput] = None
