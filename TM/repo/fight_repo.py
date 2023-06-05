import uuid
from sqlalchemy import Column, String, ForeignKey, Integer
import sqlalchemy
from sqlalchemy.dialects import postgresql

from .base import Base
from .database import SessionLocal
from ..model.status import FightStatus


class FightDTO(Base):
    __tablename__ = "fights"

    id = Column(postgresql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    fighter_1_id = Column(postgresql.UUID(as_uuid=True), ForeignKey('fighters.id'))
    fighter_2_id = Column(postgresql.UUID(as_uuid=True), ForeignKey('fighters.id'))
    status = Column(sqlalchemy.Enum(FightStatus), nullable=False)
    secretary_id = Column(String)
    current_round = Column(Integer)


def get_fight_by_id(fight_id: uuid.UUID) -> FightDTO:
    with SessionLocal() as session:
        fight_dto = session.query(FightDTO).filter(FightDTO.id == fight_id).first()
    return fight_dto


def add_fight(fight: FightDTO):
    with SessionLocal() as session:
        session.add(fight)
        session.commit()


def update_fight(fight: FightDTO):
    with SessionLocal() as session:
        res = session.query(FightDTO).filter(FightDTO.id == fight.id).first()
        res.status = fight.status
        res.current_round = fight.current_round
        res.secretary_id = fight.secretary_id
        session.commit()

def get_fights_by_fighter_id(fighter_id: UUID):
    pass
