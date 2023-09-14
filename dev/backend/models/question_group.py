# Please don't use **kwargs
# Keep the code clean and CLEAR

from typing import Optional, List
from typing_extensions import TypedDict
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from core.db import Base
from models.question import QuestionBase


class QuestionGroupDict(TypedDict):
    id: int
    form: int
    name: str
    order: Optional[int] = None


class QuestionGroup(Base):
    __tablename__ = "question_group"
    id = Column(Integer, primary_key=True, index=True, nullable=True)
    form = Column(Integer, ForeignKey('form.id'))
    name = Column(String)
    order = Column(Integer, nullable=True)
    repeatable = Column(Boolean, default=False)
    question = relationship("Question",
                            cascade="all, delete",
                            passive_deletes=True,
                            backref="question")

    def __init__(self,
                 name: str,
                 form: form,
                 order: order,
                 repeatable: Optional[bool] = False,
                 id: Optional[int] = None):
        self.id = id
        self.name = name
        self.form = form
        self.order = order
        self.repeatable = repeatable

    def __repr__(self) -> int:
        return f"<QuestionGroup {self.id}>"

    @property
    def serialize(self) -> QuestionGroupDict:
        return {
            "id": self.id,
            "form": self.form,
            "question": self.question,
            "name": self.name,
            "order": self.order,
            "repeatable": self.repeatable
        }


class QuestionGroupBase(BaseModel):
    id: int
    form: int
    name: str
    order: Optional[int] = None
    repeatable: Optional[bool] = False
    question: List[QuestionBase]

    class Config:
        orm_mode = True
