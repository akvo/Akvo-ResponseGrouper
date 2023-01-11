import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.orm import Session

pytestmark = pytest.mark.asyncio


class TestRoutes:
    @pytest.mark.asyncio
    async def test_get_index_collection(
        self, app: FastAPI, session: Session, client: AsyncClient
    ) -> None:
        response = await client.get(app.url_path_for("collection:get_index"))
        assert response.status_code == 200
        assert response.json() == [{"greeting": "Hello from collection"}]

    @pytest.mark.asyncio
    async def test_get_index_category(
        self, app: FastAPI, session: Session, client: AsyncClient
    ) -> None:
        res = await client.get(
            app.url_path_for("collection:get_index_category")
        )
        assert res.status_code == 200
