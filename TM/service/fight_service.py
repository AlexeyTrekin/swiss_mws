from uuid import UUID
from ..repo import get_fight_by_id, get_rounds_by_fight_id, update_fight, add_fight, FightDTO
from ..model import Fight
from .fighter_service import get_fighter
from .round_service import get_round, save_round


def get_fight(fight_id: UUID):
    fight_dto = get_fight_by_id(fight_id)
    fighter_1 = get_fighter(fight_dto.fighter_1_id)
    fighter_2 = get_fighter(fight_dto.fighter_2_id)
    rounds = get_rounds_by_fight_id(fight_id)

    return Fight(id=fight_dto.id,
                 fighter_1=fighter_1,
                 fighter_2=fighter_2,
                 status=fight_dto.status,
                 secretary_id=fight_dto.secretary_id,
                 current_round=fight_dto.current_round,
                 rounds=rounds)


def save_fight(fight: Fight):
    for round in fight.rounds:
        save_round(round)
    dto = FightDTO(id=fight.id,
                   fighter_1_id=fight.fighter_1.id,
                   fighter_2_id=fight.fighter_2.id,
                   status=fight.status,
                   secretary_id=fight.secretary_id,
                   current_round=fight.current_round)
    if get_fight_by_id(fight.id):
        update_fight(dto)
    else:
        add_fight(dto)
