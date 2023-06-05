from uuid import UUID, uuid4

from pydantic import BaseModel, Field
from typing import List, Optional
from .status import FightStatus
from .fight_round import FightRound
from .fighter import Fighter


class Fight(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    fighter_1: Fighter
    fighter_2: Fighter
    status = FightStatus.planned
    # todo: change to Secretary model?
    secretary_id: Optional[str] = None
    rounds_num: int = 1
    current_round: int = 0
    rounds: List[FightRound] = Field(default_factory=list)

    # === Properties that wrap around the self.rounds fields  ===
    @property
    def doubles(self):
        return sum(r.doubles for r in self.rounds)

    @property
    def warnings_1(self):
        return sum(r.warnings_1 for r in self.rounds)

    @property
    def warnings_2(self):
        return sum(r.warnings_2 for r in self.rounds)

    @property
    def total_score_1(self):
        return sum(r.score_1 for r in self.rounds)

    @property
    def total_score_2(self):
        return sum(r.score_2 for r in self.rounds)


    @property
    def result(self):
        raise NotImplementedError('The result calculation may be different depending on rules'
                                  'so it must be either implemented in inherited class'
                                  'or calculated outside of the Fight')
    # =========================================================

    def repeats(self, other):
        return {self.fighter_1.id, self.fighter_2.id} == {other.fighter_2.id, other.fighter_2.id}
