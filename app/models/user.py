from typing import Optional
from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, exclude=True)
    name: str = Field(...)
    email: str = Field(..., unique=True)
    password: str = Field(...)
