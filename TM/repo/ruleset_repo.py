import uuid
from .base import Base
from .database import SessionLocal
import sqlalchemy
from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects import postgresql


class RulesetDTO(Base):
    __tablename__ = "rules"
    id = Column(postgresql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)


def add_ruleset(dto: RulesetDTO):
    with SessionLocal() as session:
        session.add(dto)
        session.commit()


def get_ruleset_by_id(ruleset_id: uuid.UUID):
    return RulesetDTO()


def get_tournament_ruleset(tournament_id: uuid.UUID):
    return RulesetDTO()