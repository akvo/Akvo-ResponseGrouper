from sqlalchemy import Column, Integer, Text
from db.connection import Base


class Category(Base):
    __tablename__ = "ar_category"
    id = Column(Integer, primary_key=True)
    data = Column(Integer)
    name = Column(Text)
    category = Column(Text)

    def __repr__(self) -> int:
        return f"<Category {self.id}>"
