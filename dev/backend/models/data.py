# Please don't use **kwargs
# Keep the code clean and CLEAR

from datetime import datetime
from typing_extensions import TypedDict
from typing import Optional, List
from pydantic import BaseModel
from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from core.db import Base
from models.answer import AnswerDict, AnswerBase
from .form import Form
from .answer import Answer


class DataDict(TypedDict):
    id: int
    form: int
    created: Optional[str] = None
    answer: List[AnswerDict]


class DataResponse(BaseModel):
    current: int
    data: List[DataDict]
    total: int
    total_page: int


class Data(Base):
    __tablename__ = "data"
    id = Column(Integer, primary_key=True, index=True, nullable=True)
    form = Column(Integer, ForeignKey(Form.id))
    created = Column(DateTime, nullable=True)
    answer = relationship(Answer,
                          cascade="all, delete",
                          passive_deletes=True,
                          backref="answer",
                          order_by=Answer.id.asc())

    def __init__(self, name: str, form: int, created: datetime):
        self.name = name
        self.form = form
        self.created = created

    def __repr__(self) -> int:
        return f"<Data {self.id}>"

    @property
    def serialize(self) -> DataDict:
        return {
            "id": self.id,
            "form": self.form,
            "created": self.created.strftime("%B %d, %Y"),
            "answer": [a.formatted for a in self.answer],
        }


class DataBase(BaseModel):
    id: int
    form: int
    created: Optional[str] = None
    answer: List[AnswerBase]

    class Config:
        orm_mode = True
