from uuid import UUID
from ..model import FightRound
from ..repo import get_rounds_by_fight_id


def get_rounds(fight_id: UUID):
    dtos = get_rounds_by_fight_id(fight_id)
    return [FightRound(id=dto.id,
                       score_1=dto.score_1,
                       score_2=dto.score_2,
                       doubles=dto.doubles,
                       warnings_1=dto.warnings_1,
                       warnings_2=dto.warnings_2,
                       current_time=dto.current_time,
                       result_1=dto.result_1,
                       result_2=dto.result_2) for dto in dtos]
