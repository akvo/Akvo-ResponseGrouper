import sys
import pytest
import random
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.orm import Session, load_only
from AkvoResponseGrouper.views import get_categories, get_results
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
        data = get_categories(session=session, form=554360198)
        assert data[0]["form"] == 554360198

    @pytest.mark.asyncio
    async def test_views_filtering_by_name(
        self, app: FastAPI, session: Session, client: AsyncClient
    ) -> None:
        data = get_categories(session=session, name="water")
        assert data[0]["name"] == "Water"

    @pytest.mark.asyncio
    async def test_views_filtering_by_category(
        self, app: FastAPI, session: Session, client: AsyncClient
    ) -> None:
        data = get_categories(session=session, category="limited")
        assert data[0]["category"] == "Limited"

    @pytest.mark.asyncio
    async def test_views_filtering_by_data(
        self, app: FastAPI, session: Session, client: AsyncClient
    ) -> None:
        random = get_random_data(session=session)
        res = get_categories(session=session, data=str(random.data))
        assert len(res) > 0

    @pytest.mark.asyncio
    async def test_views_filtering_by_category_n_form(
        self, app: FastAPI, session: Session, client: AsyncClient
    ) -> None:
        data = get_categories(
            session=session, category="basic", form=554360198
        )
        assert data[0]["category"] == "Basic"
        assert data[0]["form"] == 554360198

    @pytest.mark.asyncio
    async def test_views_get_result_keys(
        self, app: FastAPI, session: Session, client: AsyncClient
    ) -> None:
        res = get_results(session=session)
        assert list(res.head(1).to_dict("records")[0].keys()) == [
            "id",
            "data",
            "form",
            "name",
            "category",
        ]
