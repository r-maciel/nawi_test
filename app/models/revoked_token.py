from typing import Optional
from sqlmodel import Field, SQLModel
from datetime import datetime


class RevokedToken(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    token: str = Field(unique=True)
    revoked_at: datetime = Field(default_factory=datetime.utcnow)
