import uuid
from .base import Base
from .database import SessionLocal
from sqlalchemy import Column, String
from sqlalchemy.dialects import postgresql


class FighterDTO(Base):

    __tablename__ = "fighters"

    id = Column(postgresql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = Column(String)
    last_name = Column(String)
    club = Column(String)


def get_fighter_by_id(fight_id: uuid.UUID) -> FighterDTO:
    with SessionLocal() as session:
        fight_dto = session.query(FighterDTO).filter(FighterDTO.id == fight_id).first()
    return fight_dto


def add_fight(fight: FighterDTO):
    with SessionLocal() as session:
        session.add(fight)
        session.commit()
