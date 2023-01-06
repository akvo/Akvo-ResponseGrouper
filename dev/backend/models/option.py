# Please don't use **kwargs
# Keep the code clean and CLEAR

from typing import Optional
from typing_extensions import TypedDict
from pydantic import BaseModel
from sqlalchemy import Column, ForeignKey
from sqlalchemy import Integer, String
from core.db import Base


class OptionDict(TypedDict):
    name: str
    order: Optional[int] = None


class OptionDictWithId(TypedDict):
    id: int
    name: str
    order: Optional[int] = None


class Option(Base):
    __tablename__ = "option"
    id = Column(Integer, primary_key=True, index=True, nullable=True)
    question = Column(Integer, ForeignKey('question.id'))
    name = Column(String)
    order = Column(Integer, nullable=True)

    def __init__(self,
                 name: str,
                 id: Optional[int] = None,
                 order: Optional[int] = None):
        self.id = id
        self.name = name
        self.order = order

    def __repr__(self) -> int:
        return f"<Option {self.id}>"

    @property
    def serialize(self) -> OptionDict:
        return {
            "id": self.id,
            "name": self.name,
            "order": self.order,
        }


class OptionBase(BaseModel):
    name: str
    order: Optional[int] = None

    class Config:
        orm_mode = True


class OptionBaseWithId(BaseModel):
    id: int
    name: str
    order: Optional[int] = None

    class Config:
        orm_mode = True
