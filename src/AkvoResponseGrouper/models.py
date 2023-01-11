from sqlalchemy import Column, Integer, Text
from typing_extensions import TypedDict
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Category(Base):
    __tablename__ = "ar_category"
    id = Column(Integer, primary_key=True)
    data = Column(Integer)
    name = Column(Text)
    category = Column(Text)

    def __repr__(self) -> int:
        return f"<Category {self.id}>"


class CategoryDict(TypedDict):
    id: int
    data: int
    name: str
    category: str
