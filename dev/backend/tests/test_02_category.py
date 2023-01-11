import sys
import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from AkvoResponseGrouper.cli.generate_schema import generate_schema
from AkvoResponseGrouper.views import categories
from scripts.seeder_datapoint import seed

pytestmark = pytest.mark.asyncio
sys.path.append("..")


class TestForm:
    @pytest.mark.asyncio
    async def test_category_data(
        self, app: FastAPI, session: Session, client: AsyncClient
    ) -> None:
        schema = generate_schema(file_config="/app/sources/category.json")
        session.execute(text(schema))
        res = categories.get(session=session)
        assert len(res) == 0
        seed(session=session, file_path="/app/sources/form.json", repeats=100)
        categories.refresh(session=session)
        res = categories.get(session=session)
        assert len(res) > 1
