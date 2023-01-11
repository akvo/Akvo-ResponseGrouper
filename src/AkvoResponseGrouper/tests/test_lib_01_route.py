import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.orm import Session

pytestmark = pytest.mark.asyncio

# NOTE:
# This tests is using different session from the tests session
# that you are running via ./dev/backend/tests/conftests


class TestRoutes:
    @pytest.mark.asyncio
    async def test_if_category_route_is_working(
        self, app: FastAPI, session: Session, client: AsyncClient
    ) -> None:
        res = await client.get(
            app.url_path_for("collection:get_index_category")
        )
        assert res.status_code == 200
