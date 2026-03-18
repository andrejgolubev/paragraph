import pytest
from httpx import AsyncClient, ASGITransport
from asgi_lifespan import LifespanManager

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.main import app
from backend.api.auth.validation import get_current_auth_user
from backend.api.auth.users import hash_password
from backend.api.db.models import Homework, Group, User
from backend.api.db.refresh_db import load_groups_and_dates
from backend.api.schemas.homework import HomeworkRequest
from backend.api.schemas.users import FullUserResponse, UserResponse
from backend.tests.conftest import GROUPS_INITIAL


HOMEWORK_DATE = "26.01.2026"
HOMEWORK_DATE_DV = "2026-01-26"
HOMEWORK_LESSON = 1
HOMEWORK_TEXT = "Док-во Великой т. Ферма (наизусть)"
ADMIN_GROUP = "543"


DATES_FOR_TESTS = {HOMEWORK_DATE: HOMEWORK_DATE_DV}


@pytest.fixture
async def ensure_homework_data(db: AsyncSession):
    await load_groups_and_dates(GROUPS_INITIAL, DATES_FOR_TESTS, db, refresh=False)
    await db.execute(delete(Homework))
    await db.commit()
    yield


@pytest.fixture
async def admin_user_data(db: AsyncSession, clean_users) -> dict:
    """Создаем тестового админа, чтобы проверять работу эндпоинтов сохранения д/з"""
    group = (await db.scalars(
        select(Group).where(Group.group_number == ADMIN_GROUP)
    )).first()

    user = User(
        name="Админ",
        email="admin@example.com",
        password=hash_password("SuperSecret123!"),
        role=f"admin.{ADMIN_GROUP}",
        active=True,
        group_id=group.id,
    )
    db.add(user)
    await db.commit()

   
    return UserResponse(
        email=user.email, 
        name=user.name, 
        group_id=user.group_id,
        role=user.role,
        active=user.active,
    )


@pytest.fixture
def override_admin_identity(admin_user_data):
    """
    Используем фикстуру admin_user_data , чтобы перезаписать функцию получения 
    текущего пользователя по токену и вернуть данные админа, имеющего право 
    сохранять д/з. 
    """
    async def _fake():
        return admin_user_data

    app.dependency_overrides[get_current_auth_user] = _fake
    yield
    # убираем override , чтобы не сломать приложение
    app.dependency_overrides.pop(get_current_auth_user, None)


@pytest.mark.asyncio(loop_scope="session")
async def test_save_and_get_homework(
    db: AsyncSession,
    admin_user_data: User,
    ensure_homework_data,
    override_admin_identity,
    redis_client, # чтобы не было 429
):
    """
    Проверяет работу сохранения и получения д/з.
    """
    payload = HomeworkRequest(
        group_data_value= GROUPS_INITIAL[ADMIN_GROUP],
        date_data_value= HOMEWORK_DATE_DV,
        lesson_index= HOMEWORK_LESSON,
        homework= HOMEWORK_TEXT,
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
    assert homework.homework == HOMEWORK_TEXT

    get_body = get_resp.json()
    assert get_body["homework"] == HOMEWORK_TEXT
    assert get_body["username"] == admin_user_data["username"]


@pytest.mark.asyncio(loop_scope="session")
async def test_convert_endpoints(
    db: AsyncSession, 
    ensure_homework_data,
    redis_client, # чтобы не было 429
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

