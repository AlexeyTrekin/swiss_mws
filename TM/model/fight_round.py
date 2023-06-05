from uuid import UUID, uuid4

from pydantic import BaseModel, Field
from .status import RoundStatus, Result


class FightRound(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    status: RoundStatus = RoundStatus.none
    score_1: int = 0
    score_2: int = 0
    doubles: int = 0
    warnings_1: int = 0
    warnings_2: int = 0
    current_time: int = 0
    result_1: Result = Result.none
    result_2: Result = Result.none

    class Config:
        use_enum_values = True

