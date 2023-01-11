import sys
import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.orm import Session

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
