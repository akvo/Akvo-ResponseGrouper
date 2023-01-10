from fastapi import APIRouter

router = APIRouter(
    prefix="/collection",
    tags=["Collection"],
)

@router.get(
    "/",
    name="collection:get_index",
    summary="initial index page for collection",
)
async def get_index():
    return [{
        "greeting": "Hello from collection"
    }]
