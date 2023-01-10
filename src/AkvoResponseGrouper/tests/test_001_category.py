import sys
import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.orm import Session
from ..db import crud_category

sys.path.append("..")
pytestmark = pytest.mark.asyncio


class TestCategoryRoutes:
    @pytest.mark.asyncio
    async def test_get_index_category(
        self, app: FastAPI, session: Session, client: AsyncClient
    ) -> None:
        res = await client.get(
            app.url_path_for("collection:get_index_category")
        )
        data = crud_category.get_categories(session=session)
        assert res.status_code == 200
        res = res.json()
        assert res == data
