from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from .db import get_session
from .views import (
    get_categories,
    get_group_by_category,
    get_category_by_data_ids,
    refresh_view,
)
from .models import GroupedCategory, Category, CategoryResponse

collection_route = APIRouter(
    prefix="/collection",
    tags=["AkvoResponseGrouper - Collection"],
)


@collection_route.get(
    "/categories",
    response_model=List[CategoryResponse],
    name="collection:get_index_category",
    summary="initial index page for collection",
)
async def get_index_category(
    form: Optional[int] = Query(default=None),
    name: Optional[str] = Query(default=None),
    category: Optional[str] = Query(default=None),
    data: Optional[str] = Query(default=None),
    session: Session = Depends(get_session),
):
    res = get_categories(
        form=form, name=name, category=category, session=session
    )
    if data:
        data = [int(d) for d in data.split(",")]
        res = get_category_by_data_ids(session=session, ids=data)
    res = [Category.res_serialize(r) for r in res]
    return res


@collection_route.get(
    "/categories/groups",
    response_model=List[GroupedCategory],
    name="collection:get_grouped_categories",
    summary="get grouped categories",
)
async def get_grouped_categories(
    form_id: Optional[int] = Query(default=None),
    category_name: Optional[str] = Query(default=None),
    session: Session = Depends(get_session),
):
    res = get_group_by_category(
        session=session, form_id=form_id, category_name=category_name
    )
    return res


@collection_route.get(
    "/refresh",
    summary="refresh materialized view",
    name="collection:refresh_materialized_view",
    tags=["Data"],
)
def refresh_materialized_view(
    session: Session = Depends(get_session),
):
    refresh_view(session=session)
    return "OK"
