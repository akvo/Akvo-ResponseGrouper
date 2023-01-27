import sys
import pytest
import random
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.orm import Session, load_only
from AkvoResponseGrouper.views import get_categories
from AkvoResponseGrouper.models import Category

pytestmark = pytest.mark.asyncio
sys.path.append("..")


def get_random_data(session: Session):
    return random.choice(
        session.query(Category).options(load_only("data")).all()
    )


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

    @pytest.mark.asyncio
    async def test_views_filtering_by_data(
        self, app: FastAPI, session: Session, client: AsyncClient
    ) -> None:
        random = get_random_data(session=session)
        res = get_categories(session=session, data=random.data)
        assert len(res) > 0
