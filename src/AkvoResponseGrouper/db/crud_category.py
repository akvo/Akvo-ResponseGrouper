from typing import List
from sqlalchemy.orm import Session
from ..models.Category import Category, CategoryDict


def get_categories(session: Session) -> List[CategoryDict]:
    return session.query(Category).all()
