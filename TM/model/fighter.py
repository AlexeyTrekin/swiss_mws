from uuid import UUID, uuid4
from typing import Optional
from pydantic import BaseModel, Field


class Fighter(BaseModel):
    __tablename__ = "rules"

    id = Column(postgresql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name: str
    last_name: str
    club: Optional[str] = None
    # todo: add club, country, etc. as Models
    # todo: add global rating and division

    def __eq__(self, other):
        """
        The fighters are compared by ID only
        :param other:
        :return:
        """
        return self.id == other.id

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
