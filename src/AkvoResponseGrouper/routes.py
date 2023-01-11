from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
from .db import get_session
from .views import get_categories

collection_route = APIRouter(
    prefix="/collection",
    tags=["AkvoResponseGrouper - Collection"],
)


@collection_route.get(
    "/",
    name="collection:get_index",
    summary="initial index page for collection",
)
async def get_index():
    return [{"greeting": "Hello from collection"}]


@collection_route.get(
    "/categories",
    name="collection:get_index_category",
    summary="get all category items",
)
async def get_index_category(
    id: Optional[int] = Query(default=None),
    data: Optional[int] = Query(default=None),
    name: Optional[str] = Query(default=None),
    category: Optional[str] = Query(default=None),
    session: Session = Depends(get_session),
):
    res = get_categories(
        id=id, data=data, name=name, category=category, session=session
    )
    return res
