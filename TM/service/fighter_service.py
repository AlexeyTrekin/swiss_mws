from uuid import UUID, uuid4
from ..model import Fighter
from ..repo import get_fighter_by_id, FighterDTO, add_fighter
from ..rest.json import CreateFighterJson

def get_fighter(fighter_id: UUID):
    dto = get_fighter_by_id(fighter_id)
    return Fighter(id=dto.id,
                   first_name=dto.first_name,
                   last_name=dto.last_name,
                   club=dto.club)


def create_fighter(fighter: CreateFighterJson):
    fighter_id = uuid4()
    dto = FighterDTO()