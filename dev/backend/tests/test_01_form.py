import sys
import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.orm import Session
from scripts.seeder_form import seed
from models.form import Form

pytestmark = pytest.mark.asyncio
sys.path.append("..")


class TestForm:
    @pytest.mark.asyncio
    async def test_if_form_seeder_is_working(
        self, app: FastAPI, session: Session, client: AsyncClient
    ) -> None:
        seed(session=session, file_path="./sources/form.json", )
        forms = session.query(Form).all()
        assert len(forms) == 1
        for form in forms:
            assert list(form.serialize) == ["id", "name", "question_group"]
