import uuid
from .base import Base
from .database import SessionLocal
import sqlalchemy
from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects import postgresql

from ..model import Status


class StagetDTO(Base):
    __tablename__ = "stages"
    id = Column(postgresql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tournament_id = Column(postgresql.UUID(as_uuid=True), ForeignKey('tournaments.id'))
    ruleset_id = Column(postgresql.UUID(as_uuid=True), ForeignKey('rulesets.id'))
    status = Column(sqlalchemy.Enum(Status), nullable=False)


def add_stage(dto: StagetDTO):
    with SessionLocal() as session:
        session.add(dto)
        session.commit()
