from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from sqlalchemy.sql.operators import ilike_op
from .models import Category, CategoryDict


def get_categories(
    session: Session,
    id: Optional[int] = None,
    data: Optional[int] = None,
    name: Optional[int] = None,
    category: Optional[int] = None,
) -> List[CategoryDict]:
    queries = []
    if id:
        queries.append(Category.id == id)
    if data:
        queries.append(Category.data == data)
    if name:
        queries.append(func.lower(Category.name) == func.lower(name))
    if category:
        queries.append(ilike_op(Category.category, f"%{category}%"))

    return session.query(Category).filter(*queries).all()


def refresh_view(session: Session):
    session.execute("REFRESH MATERIALIZED VIEW ar_category;")
