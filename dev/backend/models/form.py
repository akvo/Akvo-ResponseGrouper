# Please don't use **kwargs
# Keep the code clean and CLEAR

from typing_extensions import TypedDict
from typing import List, Optional
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from core.db import Base
from models.question_group import QuestionGroupBase


class FormDict(TypedDict):
    id: int
    name: str


class FormDictWithFlag(TypedDict):
    id: int
    name: str


class Form(Base):
    __tablename__ = "form"
    id = Column(Integer, primary_key=True, index=True, nullable=True)
    name = Column(String)
    question_group = relationship("QuestionGroup",
                                  cascade="all, delete",
                                  passive_deletes=True,
                                  backref="question_group")

    def __init__(
        self,
        id: Optional[int],
        name: str,
    ):
        self.id = id
        self.name = name

    def __repr__(self) -> int:
        return f"<Form {self.id}>"

    @property
    def serialize(self) -> FormDict:
        return {
            "id": self.id,
            "name": self.name,
            "version": self.version,
            "question_group": self.question_group,
        }


class FormBase(BaseModel):
    id: int
    name: str
    question_group: List[QuestionGroupBase]

    class Config:
        orm_mode = True
