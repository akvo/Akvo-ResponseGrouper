import sys
import pytest
from os.path import exists
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from sqlalchemy import create_engine

from ..core.db import get_db_url

from AkvoResponseGrouper.cli.generate_schema import generate_schema
from AkvoResponseGrouper.views import (
    get_categories,
    get_data_categories,
    refresh_view,
)
from scripts.seeder_datapoint import seed
from AkvoResponseGrouper.db import validate_question_options, get_questions

pytestmark = pytest.mark.asyncio
sys.path.append("..")


class TestMigration:
    @pytest.mark.asyncio
    async def test_if_views_is_successfully_added(
        self, app: FastAPI, session: Session, client: AsyncClient
    ) -> None:
        schema = generate_schema(file_config="./sources/category.json")
        session.execute(text(schema))
        # check if .category.json was created
        assert exists("./.category.json") is True
        # BEFORE
        res = get_data_categories(session=session)
        assert len(res) == 0
        # SEED DATA
        seed(session=session, repeats=100)
        # AFTER REFRESH
        refresh_view(session=session)
        res = get_categories(session=session)
        assert len(res) > 1

    @pytest.mark.asyncio
    async def test_if_question_n_options_exists(
        self, app: FastAPI, session: Session, client: AsyncClient
    ) -> None:
        engine = create_engine(get_db_url())
        with engine.connect() as connection:
            gq = get_questions(connection=connection)
            assert len(gq) > 0
            ce = validate_question_options(
                connection=connection, question=1, form=1, options=["Yes"]
            )
            assert ce == []
            cy = validate_question_options(
                connection=connection,
                question=567800083,
                form=554360198,
                options=["Yes"],
            )
            assert cy == ["Yes"]
            cn = validate_question_options(
                connection=connection,
                question=567800080,
                form=554360198,
                options=None,
            )
            assert cn == [1]
