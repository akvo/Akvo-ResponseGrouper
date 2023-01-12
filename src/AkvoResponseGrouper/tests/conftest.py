import pytest
from os import environ
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from asgi_lifespan import LifespanManager
from AkvoResponseGrouper.db import get_session, get_db_url
from AkvoResponseGrouper.models import Base
from AkvoResponseGrouper.routes import collection_route

environ["APP_ENV"] = "test"


@pytest.fixture
def app() -> FastAPI:
    app = FastAPI()
    app.include_router(collection_route)
    engine = create_engine(get_db_url())
    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(
        autocommit=False, autoflush=False, bind=engine
    )

    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_session] = override_get_db
    return app


@pytest.fixture
def session() -> Session:
    engine = create_engine(get_db_url())
    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(
        autocommit=False, autoflush=False, bind=engine
    )
    return TestingSessionLocal()


@pytest.fixture
async def client(app: FastAPI) -> AsyncClient:
    async with LifespanManager(app):
        async with AsyncClient(
            app=app, base_url="http://testserver"
        ) as client:
            yield client
