from sqlalchemy import Column, Integer, Text
from typing_extensions import TypedDict
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel
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


class CategoryResponse(TypedDict):
    form: int
    data: int
    name: str
    category: str


class Category(Base):
    __tablename__ = "ar_category"
    id = Column(Integer, primary_key=True)
    form = Column(Integer)
    data = Column(Integer)
    name = Column(Text)
    category = Column(Text)

    def __repr__(self) -> int:
        return f"<Category {self.id}>"

    def group_serialize(data) -> GroupByDict:
        return {
            "category": data.category,
            "name": data.name,
            "count": data.count,
        }

    def res_serialize(data) -> CategoryResponse:
        return {
            "data": data.data,
            "form": data.form,
            "name": data.name,
            "category": data.category,
        }

    @property
    def serialize(self) -> CategoryDict:
        return {
            "id": self.id,
            "data": self.data,
            "form": self.form,
            "name": self.name,
            "category": self.category,
        }


class CountedCategory(TypedDict):
    name: str
    count: int


class GroupedCategory(BaseModel):
    category: str
    options: List[CountedCategory]
