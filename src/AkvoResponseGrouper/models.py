from sqlalchemy import Column, Integer, JSON
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
    category: str


class CategoryModelDict(TypedDict):
    id: int
    data: int
    form: int
    opt: dict


class Category(Base):
    __tablename__ = "ar_category"
    id = Column(Integer, primary_key=True)
    form = Column(Integer)
    data = Column(Integer)
    opt = Column(JSON)

    def __repr__(self) -> int:
        return f"<Category {self.id}>"

    def group_serialize(data) -> GroupByDict:
        return {
            "category": data.category,
            "name": data.name,
            "count": data.count,
        }

    @property
    def serialize(self) -> CategoryModelDict:
        return {
            "id": self.id,
            "form": self.form,
            "data": self.data,
            "opt": self.opt,
        }


class CountedCategory(TypedDict):
    name: str
    count: int


class GroupedCategory(TypedDict):
    form: int
    categories: List[CountedCategory]
