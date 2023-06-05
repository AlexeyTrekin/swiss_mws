from typing import Optional
from pydantic import BaseModel


class CreateFighterJson(BaseModel):
    first_name: str
    last_name: str
    club: Optional[str] = None
