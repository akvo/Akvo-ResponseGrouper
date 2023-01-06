# Please don't use **kwargs
# Keep the code clean and CLEAR

import enum
from typing import Optional, List
from typing_extensions import TypedDict
from pydantic import BaseModel
from sqlalchemy import Column, ForeignKey
from sqlalchemy import Integer, String, Enum
from sqlalchemy.orm import relationship
from core.db import Base
from models.option import OptionBase, OptionBaseWithId


class QuestionType(enum.Enum):
    text = 'text'
    number = 'number'
    option = 'option'
    multiple_option = 'multiple_option'
    photo = 'photo'
    date = 'date'
    geo = 'geo'
    administration = 'administration'


class DependencyDict(TypedDict):
    id: int
    options: List[str]


class QuestionDict(TypedDict):
    id: int
    form: int
    question_group: int
    order: Optional[int] = None
    name: str
    type: QuestionType
    option: Optional[List[OptionBase]] = None


class Question(Base):
    __tablename__ = "question"
    id = Column(Integer, primary_key=True, index=True, nullable=True)
    form = Column(Integer, ForeignKey('form.id'))
    question_group = Column(Integer, ForeignKey('question_group.id'))
    name = Column(String)
    order = Column(Integer, nullable=True)
    type = Column(Enum(QuestionType), default=QuestionType.text)
    option = relationship("Option",
                          cascade="all, delete",
                          passive_deletes=True,
                          backref="option")

    def __init__(self, id: Optional[int], name: str, order: int, form: int,
                 question_group: int, type: QuestionType):
        self.id = id
        self.form = form
        self.order = order
        self.question_group = question_group
        self.name = name
        self.type = type

    def __repr__(self) -> int:
        return f"<Question {self.id}>"

    @property
    def serialize(self) -> QuestionDict:
        return {
            "id": self.id,
            "form": self.form,
            "question_group": self.question_group,
            "name": self.name,
            "order": self.order,
            "type": self.type,
            "option": self.option,
        }


class QuestionBase(BaseModel):
    id: int
    form: int
    question_group: int
    name: str
    order: Optional[int] = None
    type: QuestionType
    option: List[OptionBaseWithId]

    class Config:
        orm_mode = True
