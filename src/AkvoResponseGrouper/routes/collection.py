from fastapi import APIRouter

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
    return [{
        "greeting": "Hello from collection"
    }]
