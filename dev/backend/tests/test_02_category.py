import sys
import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from AkvoResponseGrouper.cli.generate_schema import generate_schema
from AkvoResponseGrouper.views import get_categories, refresh_view
from scripts.seeder_datapoint import seed

pytestmark = pytest.mark.asyncio
sys.path.append("..")


class TestMigration:
    @pytest.mark.asyncio
    async def test_if_views_is_successfully_added(
        self, app: FastAPI, session: Session, client: AsyncClient
    ) -> None:
        schema, query = generate_schema(file_config="./sources/category.json")
        session.execute(text(schema))
        # BEFORE
        res = get_categories(session=session)
        assert len(res) == 0
        # SEED DATA
        seed(session=session, file_path="./sources/form.json", repeats=100)
        # AFTER REFRESH
        refresh_view(session=session)
        res = get_categories(session=session)
        assert len(res) > 1
