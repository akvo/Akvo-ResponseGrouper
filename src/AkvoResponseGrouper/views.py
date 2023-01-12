from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from sqlalchemy.sql.operators import ilike_op
from .models import Category, CategoryDict


def get_categories(
    session: Session,
    form: Optional[int] = None,
    name: Optional[int] = None,
    category: Optional[int] = None,
) -> List[CategoryDict]:
    queries = []
    if form:
        queries.append(Category.form == form)
    if name:
        queries.append(func.lower(Category.name) == func.lower(name))
    if category:
        queries.append(ilike_op(Category.category, f"%{category}%"))

    return session.query(Category).filter(*queries).all()


def refresh_view(session: Session):
    session.execute("REFRESH MATERIALIZED VIEW ar_category;")
