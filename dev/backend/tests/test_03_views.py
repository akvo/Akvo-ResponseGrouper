import sys
import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.orm import Session
from scripts.seeder_datapoint import seed
from AkvoResponseGrouper.views import get_categories

pytestmark = pytest.mark.asyncio
sys.path.append("..")


class TestViews:
    @pytest.mark.asyncio
    async def test_views_filtering_by_form(
        self, app: FastAPI, session: Session, client: AsyncClient
    ) -> None:
        res = get_categories(session=session, form=1)
        data = [r.serialize for r in res]
        assert data[0]["form"] == 1

    @pytest.mark.asyncio
    async def test_views_filtering_by_name(
        self, app: FastAPI, session: Session, client: AsyncClient
    ) -> None:
        res = get_categories(session=session, name="category 1")
        data = [r.serialize for r in res]
        assert data[0]["name"] == "Category 1"

    @pytest.mark.asyncio
    async def test_views_filtering_by_category(
        self, app: FastAPI, session: Session, client: AsyncClient
    ) -> None:
        res = get_categories(session=session, category="non-rural female head")
        data = [r.serialize for r in res]
        assert data[0]["category"] == "Non-Rural Female Head"
