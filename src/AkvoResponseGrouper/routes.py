from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from .db import get_session
from .views import get_categories, get_group_by_category
from .models import GroupedCategory

collection_route = APIRouter(
    prefix="/collection",
    tags=["AkvoResponseGrouper - Collection"],
)


@collection_route.get(
    "/",
    name="collection:get_index_category",
    summary="initial index page for collection",
)
async def get_index_category(
    form: Optional[int] = Query(default=None),
    name: Optional[str] = Query(default=None),
    category: Optional[str] = Query(default=None),
    data: Optional[int] = Query(default=None),
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
    form_id: Optional[int] = Query(default=None),
    category_name: Optional[str] = Query(default=None),
    session: Session = Depends(get_session),
):
    res = get_group_by_category(
        session=session, form_id=form_id, category_name=category_name
    )
    return res
