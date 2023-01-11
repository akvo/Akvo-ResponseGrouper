from fastapi import FastAPI
from .routes import collection_route


def get_application() -> FastAPI:
    application = FastAPI()

    application.include_router(collection_route)

    return application
