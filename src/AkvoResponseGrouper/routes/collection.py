from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session
from ..db.connection import get_session
from ..db.crud_category import get_categories

collection_route = APIRouter(
    prefix="/collection",
    tags=["Collection"],
)


@collection_route.get(
    "/",
    name="collection:get_index",
    summary="initial index page for collection",
)
async def get_index():
    return [{"greeting": "Hello from collection"}]


@collection_route.get(
    "/categories/",
    name="collection:get_index_categories",
    summary="get all category items",
)
async def get_index_categories(session: Session = Depends(get_session)):
    data = get_categories(session=session)
    return data
