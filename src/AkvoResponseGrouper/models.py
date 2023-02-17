from sqlalchemy import Column, Integer, Text, JSON
from typing_extensions import TypedDict
from sqlalchemy.ext.declarative import declarative_base
from typing import List

Base = declarative_base()


class GroupByDict(TypedDict):
    category: str
    name: str
    count: int


class CategoryDict(TypedDict):
    id: int
    data: int
    form: int
    name: str
    category: str


class CategoryModelDict(TypedDict):
    id: int
    data: int
    form: int
    name: str
    opt: dict


class Category(Base):
    __tablename__ = "ar_category"
    id = Column(Integer, primary_key=True)
    form = Column(Integer)
    data = Column(Integer)
    name = Column(Text)
    opt = Column(JSON)

    def __repr__(self) -> int:
        return f"<Category {self.id}>"

    @property
    def serialize(self) -> CategoryModelDict:
        return {
            "id": self.id,
            "data": self.data,
            "form": self.form,
            "name": self.name,
            "opt": self.opt,
        }


class CountedCategory(TypedDict):
    name: str
    count: int


class GroupedCategory(TypedDict):
    category: str
    form: int
    options: List[CountedCategory]
