import pytest
from os import environ
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.orm import Session
from ..db.connection import SessionLocal
from ..main import get_application

environ["APP_ENV"] = "test"


@pytest.fixture
def app() -> FastAPI:
    return get_application()


@pytest.fixture(scope="session")
async def client() -> AsyncClient:
    async with AsyncClient(
        app=get_application(),
        base_url="http://test",
        headers={"Content-Type": "application/json"},
    ) as client:
        yield client


@pytest.fixture
def session() -> Session:
    session = SessionLocal()
    return session
