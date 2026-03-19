import pytest
from httpx import AsyncClient, ASGITransport
from asgi_lifespan import LifespanManager

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.main import app
from backend.api.db.models import Homework, User
from backend.api.db.refresh_db import load_groups_and_dates
from backend.api.schemas.homework import HomeworkRequest
from backend.tests.conftest import (
    GROUPS_INITIAL,
    HOMEWORK_DATE,
    HOMEWORK_DATE_DV,
    HOMEWORK_LESSON,
    HOMEWORK_TEXT,
    ADMIN_GROUP,
)


DATES_FOR_TESTS = {HOMEWORK_DATE: HOMEWORK_DATE_DV}


@pytest.fixture
async def ensure_homework_data(db: AsyncSession):
    await load_groups_and_dates(GROUPS_INITIAL, DATES_FOR_TESTS, db, refresh=False)
    await db.execute(delete(Homework))
    await db.commit()
    yield


@pytest.mark.asyncio(loop_scope="session")
async def test_save_and_get_homework(
    db: AsyncSession,
    admin_user_data: User,
    ensure_homework_data,
    override_admin_identity,
    redis_client,  # чтобы не было 429
):
    """
    Проверяет работу сохранения и получения д/з.
    """
    payload = HomeworkRequest(
        group_data_value=GROUPS_INITIAL[ADMIN_GROUP],
        date_data_value=HOMEWORK_DATE_DV,
        lesson_index=HOMEWORK_LESSON,
        homework_text=HOMEWORK_TEXT,
    ).model_dump()

    async with LifespanManager(app):
        async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test",
        ) as client:

            save_resp = await client.post("/homework/save", json=payload)

            get_resp = await client.get(
                "/homework/get",
                params={
                    "group_data_value": payload["group_data_value"],
                    "date_data_value": payload["date_data_value"],
                    "lesson_index": HOMEWORK_LESSON,
                },
            )

    assert save_resp.status_code == 200

    homework = (await db.scalars(select(Homework))).first()
    assert homework is not None
    assert homework.homework_text == HOMEWORK_TEXT

    get_body = get_resp.json()
    assert get_body["homework"] == HOMEWORK_TEXT
    assert get_body["username"] == admin_user_data["username"]


@pytest.mark.asyncio(loop_scope="session")
async def test_convert_endpoints(
    db: AsyncSession,
    ensure_homework_data,
    redis_client,  # чтобы не было 429
):
    """
    Проверяет работу эндпоинтов, конвертирующих даты/группы в соответствующие
    им data_value
    """
    async with LifespanManager(app):
        async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test",
        ) as client:

            convert_resp = await client.get(
                "/homework/convert",
                params={"group_number": ADMIN_GROUP, "date": HOMEWORK_DATE},
            )

            convert_back_resp = await client.get(
                "/homework/convert-back",
                params={
                    "group_data_value": GROUPS_INITIAL[ADMIN_GROUP],
                    "date_data_value": HOMEWORK_DATE_DV,
                },
            )

    assert convert_resp.status_code == 200
    assert convert_resp.json()["group_data_value"] == GROUPS_INITIAL[ADMIN_GROUP]
    assert convert_resp.json()["date_data_value"] == HOMEWORK_DATE_DV

    assert convert_back_resp.status_code == 200
    assert convert_back_resp.json()["group_number"] == ADMIN_GROUP
    assert convert_back_resp.json()["date"] == HOMEWORK_DATE
