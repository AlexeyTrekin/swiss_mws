import uuid
from .base import Base
from .database import SessionLocal
import sqlalchemy
from sqlalchemy import Column
from sqlalchemy.dialects import postgresql
from ..model.status import Status


class TournamentDTO(Base):
    __tablename__ = "tournaments"
    id = Column(postgresql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    status = Column(sqlalchemy.Enum(Status), nullable=False)


def add_tournament(dto: TournamentDTO):
    with SessionLocal() as session:
        session.add(dto)
        session.commit()


def get_tournament(dto: TournamentDTO):
    with SessionLocal() as session:
        dto = session.query(TournamentDTO).filter(TournamentDTO.id == tournament_id).first()
    return dto


def update_tournament_status(tournament_id: uuid.UUID,
                             status: Status):
    with SessionLocal() as session:
        res = session.query(TournamentDTO).filter(TournamentDTO.id == tournament_id).first()
        res.status = status
        session.commit()
