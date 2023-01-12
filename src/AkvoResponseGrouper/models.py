from sqlalchemy import Column, Integer, Text
from typing_extensions import TypedDict
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Category(Base):
    __tablename__ = "ar_category"
    id = Column(Integer, primary_key=True)
    form = Column(Integer)
    data = Column(Integer)
    name = Column(Text)
    category = Column(Text)

    def __repr__(self) -> int:
        return f"<Category {self.id}>"


class CategoryDict(TypedDict):
    id: int
    data: int
    form: int
    name: str
    category: str
