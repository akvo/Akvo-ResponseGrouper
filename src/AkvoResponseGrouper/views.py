from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_
from sqlalchemy.sql.operators import ilike_op
from .models import Category, CategoryDict
from .utils import grouped_items


def get_categories(
    session: Session,
    form: Optional[int] = None,
    name: Optional[str] = None,
    category: Optional[str] = None,
    data: Optional[int] = None,
) -> List[CategoryDict]:
    queries = []
    if form:
        queries.append(Category.form == form)
    if name:
        queries.append(func.lower(Category.name) == func.lower(name))
    if category:
        queries.append(ilike_op(Category.category, f"%{category}%"))
    if data:
        queries.append(Category.data == data)
    return session.query(Category).filter(*queries).all()


def get_by_group_category(
    session: Session,
    category_name: Optional[str] = None,
    form_id: Optional[int] = None,
):
    result = (
        session.query(
            Category.category,
            Category.name,
            func.count(Category.data).label("count"),
        )
        .filter(
            or_(
                category_name is None,
                and_(
                    category_name is not None,
                    ilike_op(Category.name, f"%{category_name}%"),
                ),
            ),
            or_(
                form_id is None,
                and_(form_id is not None, Category.form == form_id),
            ),
        )
        .group_by(Category.category)
        .group_by(Category.name)
        .all()
    )
    result = grouped_items(result)
    return result


def refresh_view(session: Session):
    session.execute("REFRESH MATERIALIZED VIEW ar_category;")
