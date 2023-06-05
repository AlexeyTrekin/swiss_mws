from uuid import UUID

from .base import Base
from .database import SessionLocal


class RoundDTO(Base):
    # todo: implement Round DB representation
    pass


def get_rounds_by_fight_id(fight_id: UUID):
    """
    SELECT * FROM round WHERE round.fight_id = fight_id ORDER_BY round.number
    """
    return
