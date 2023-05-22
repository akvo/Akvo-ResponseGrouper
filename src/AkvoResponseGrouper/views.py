from typing import List, Optional
from sqlalchemy import func
from sqlalchemy.orm import Session
from .models import Category, CategoryDict
from .utils import transform_categories_to_df, get_counted_category


def get_data_categories(
    session: Session,
    form: Optional[int] = None,
    name: Optional[str] = None,
    data: Optional[List[int]] = None,
):
    queries = []
    if form:
        queries.append(Category.form == form)
    if name:
        queries.append(func.lower(Category.name) == name.lower())
    if data:
        queries.append(Category.data.in_(data))
    categories = session.query(Category).filter(*queries).all()
    categories = [c.serialize for c in categories]
    return categories


def get_results(session: Session):
    categories = get_data_categories(session=session)
    return transform_categories_to_df(categories=categories)


def get_categories(
    session: Session,
    form: Optional[int] = None,
    name: Optional[str] = None,
    category: Optional[str] = None,
    data: Optional[List[int]] = None,
) -> List[CategoryDict]:
    categories = get_data_categories(
        session=session, form=form, name=name, data=data
    )
    df = transform_categories_to_df(categories=categories)
    if category:
        df = df.query(f"category.str.lower() == '{category.lower()}'")
    return df.to_dict("records")


def get_group_by_category(
    session: Session,
    category: Optional[str] = None,
    form: Optional[int] = None,
):
    res = get_results(session=session)
    queries = []
    if form:
        queries.append(f"form == {form}")
    if category:
        queries.append(f"category.str.lower() == '{category.lower()}'")
    if len(queries):
        queries = " & ".join(queries)
        res = res.query(queries)
    return get_counted_category(df=res)


def refresh_view(session: Session):
    session.execute("REFRESH MATERIALIZED VIEW ar_category;")
    session.commit()
