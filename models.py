from sqlmodel import SQLModel, Field
from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime

class PostBase(SQLModel):
    title: str
    content: str


class Post(PostBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    creation_date: date = Field(default_factory=date.today)


class PostUpdate(BaseModel):
    title: str = None
    content: str = None