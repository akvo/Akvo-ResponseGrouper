# Please don't use **kwargs
# Keep the code clean and CLEAR

from typing_extensions import TypedDict
from typing import Optional, List, Union
from .question import QuestionType
from pydantic import BaseModel
from sqlalchemy import Column, Integer, Float, Text, String
from sqlalchemy import ForeignKey
import sqlalchemy.dialects.postgresql as pg
from core.db import Base


class AnswerDict(TypedDict):
    question: int
    value: Union[int, float, str, bool, dict, List[str], List[int],
                 List[float], None]


class Answer(Base):
    __tablename__ = "answer"
    id = Column(Integer, primary_key=True, index=True, nullable=True)
    question = Column(Integer,
                      ForeignKey('question.id',
                                 onupdate="CASCADE",
                                 ondelete="CASCADE"),
                      primary_key=True)
    data = Column(Integer,
                  ForeignKey('data.id', onupdate="CASCADE",
                             ondelete="CASCADE"),
                  primary_key=True)
    text = Column(Text, nullable=True)
    value = Column(Float, nullable=True)
    options = Column(pg.ARRAY(String), nullable=True)

    def __init__(self,
                 question: int,
                 data: Optional[int] = None,
                 text: Optional[str] = None,
                 value: Optional[float] = None,
                 options: Optional[List[str]] = None):
        self.question = question
        self.data = data
        self.text = text
        self.value = value
        self.options = options

    def __repr__(self) -> int:
        return f"<Answer {self.id}>"

    @property
    def serialize(self) -> AnswerDict:
        return {
            "id": self.id,
            "question": self.question,
            "data": self.data,
            "text": self.text,
            "value": self.value,
            "options": self.options,
        }

    @property
    def formatted(self) -> AnswerDict:
        answer = {
            "question": self.question,
        }
        type = self.question_detail.type
        if type in [
                QuestionType.administration, QuestionType.number,
                QuestionType.answer_list
        ]:
            answer.update({"value": self.value})
        if type in [QuestionType.text, QuestionType.geo, QuestionType.date]:
            answer.update({"value": self.text})
        if type == QuestionType.option:
            answer.update({"value": self.options[0]})
        if type == QuestionType.multiple_option:
            answer.update({"value": self.options})
        if type == QuestionType.photo:
            answer.update({"value": self.value})
        return answer


class AnswerBase(BaseModel):
    id: int
    question: int
    data: int
    text: Optional[str] = None
    value: Optional[float] = None
    options: Optional[List[str]] = None

    class Config:
        orm_mode = True
