import sys
import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.orm import Session

pytestmark = pytest.mark.asyncio
sys.path.append("..")


class TestCollection:
    @pytest.mark.asyncio
    async def test_seed_form(
        self, app: FastAPI, session: Session, client: AsyncClient
    ) -> None:
        response = await client.get(app.url_path_for("collection:get_index"))
        assert response.status_code == 200
        assert response.json() == [{"greeting": "Hello from collection"}]
