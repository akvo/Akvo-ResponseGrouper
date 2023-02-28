from os import environ
from fastapi import APIRouter, Depends, Query, BackgroundTasks
from sqlalchemy.orm import Session
from typing import Optional, List
from .db import get_session
from .views import (
    get_categories,
    get_group_by_category,
    refresh_view,
)
from .models import GroupedCategory, CategoryDict
from .utils import group_by_category_output

collection_route = APIRouter(
    prefix="/collection",
    tags=["AkvoResponseGrouper - Collection"],
)


@collection_route.get(
    "/categories",
    response_model=List[CategoryDict],
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
        form=form, name=name, category=category, data=data, session=session
    )
    return res


@collection_route.get(
    "/categories/groups",
    response_model=List[GroupedCategory],
    name="collection:get_grouped_categories",
    summary="get grouped categories",
)
async def get_grouped_categories(
    form: Optional[int] = Query(default=None),
    category: Optional[str] = Query(default=None),
    session: Session = Depends(get_session),
):
    res = get_group_by_category(session=session, form=form, category=category)
    res = group_by_category_output(res)
    return res


@collection_route.get(
    "/refresh",
    summary="refresh materialized view",
    name="collection:refresh_materialized_view",
)
def refresh_materialized_view(
    background_tasks: BackgroundTasks,
    session: Session = Depends(get_session),
):
    TESTING = environ.get("TESTING")
    if not TESTING:
        background_tasks.add_task(refresh_view, session=session)
    return "OK"
