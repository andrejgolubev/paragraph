from httpx import ASGITransport, AsyncClient
import pytest, subprocess

from sqlalchemy import delete, select, text
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.db.models import User
from backend.api.db.database import AsyncSessionLocalTest
from backend.api.main import app as main_app

from asgi_lifespan import LifespanManager
from redis.asyncio import Redis
from backend.api.auth.validation import get_current_auth_user
from backend.api.auth.users import hash_password
from backend.api.db.models import Group, User
from backend.api.schemas.users import UserResponse

base_url = 'http://test'

HOMEWORK_DATE = "26.01.2026"
HOMEWORK_DATE_DV = "2026-01-26"
HOMEWORK_LESSON = 1
HOMEWORK_TEXT = "Док-во Великой т. Ферма (наизусть)"
ADMIN_GROUP = "543"
ADMIN_PASSWORD = "SuperSecret123!"


GROUPS_INITIAL = { 
    "543": "1639", 
    "5413": "1638", 
    "543М": "1640",
    "5413М": "1634",
    "5423": "1638", 
}

@pytest.fixture(scope='session', autouse=True)
def storage_setup():
    """
    Подгатавливает Postgres к прогонке тестовых данных. 
    """
    subprocess.check_call(["poetry", "run", "alembic", "upgrade", "head"])


@pytest.fixture
async def db(): 
    async with AsyncSessionLocalTest() as session:
        yield session
        

@pytest.fixture
async def clean_users(db: AsyncSession):
    """Очищает таблицу users перед и после тестов"""
    await db.execute(delete(User))
    await db.commit()
    yield
    await db.execute(delete(User))
    await db.commit()


@pytest.fixture(scope='function')
async def redis_client() -> Redis:
    async with LifespanManager(main_app):
        redis: Redis = main_app.state.redis
        await redis.flushall()
        await redis.ping()
        return redis


# @pytest.fixture(scope='session')
# async def current_user() -> User: 
#     async with AsyncClient(
#             transport=ASGITransport(app=main_app), 
#             base_url=base_url
#         ) as client:
#             response = await client.post("/user/register", json=register_payload)        
        
@pytest.fixture
async def admin_user_data(db: AsyncSession, clean_users) -> dict:
    """Создаем тестового админа, чтобы проверять работу эндпоинтов сохранения д/з"""
    group = (await db.scalars(
        select(Group).where(Group.group_number == ADMIN_GROUP)
    )).first()

    user = User(
        name="Админ",
        email="admin@example.com",
        password=hash_password(ADMIN_PASSWORD),
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

    main_app.dependency_overrides[get_current_auth_user] = _fake
    yield
    # убираем override , чтобы не сломать приложение
    main_app.dependency_overrides.pop(get_current_auth_user, None)





