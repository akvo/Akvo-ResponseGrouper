import sys
import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.orm import Session
from AkvoResponseGrouper.db import view_exist

pytestmark = pytest.mark.asyncio
sys.path.append("..")


class TestRouteCollection:
    @pytest.mark.asyncio
    async def test_if_route_successfully_attached(
        self, app: FastAPI, session: Session, client: AsyncClient
    ) -> None:
        response = await client.get(
            app.url_path_for("collection:get_index_category")
        )
        assert response.status_code == 200

    async def test_if_grouped_categories_route_successfully_added(
        self, app: FastAPI, session: Session, client: AsyncClient
    ) -> None:
        response = await client.get(
            app.url_path_for("collection:get_grouped_categories")
        )
        assert response.status_code == 200

    async def test_if_refresh_route_successfully_added(
        self, app: FastAPI, session: Session, client: AsyncClient
    ) -> None:
        response = await client.get(
            app.url_path_for("collection:refresh_materialized_view")
        )
        assert response.status_code == 200

    async def test_if_view_is_exists(
        self, app: FastAPI, session: Session, client: AsyncClient
    ) -> None:
        assert view_exist() is True
