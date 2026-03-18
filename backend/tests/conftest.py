from httpx import ASGITransport, AsyncClient
import pytest, subprocess

from sqlalchemy import delete, text
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.db.models import User
from backend.core.config import settings
from backend.api.db.database import AsyncSessionLocalTest
from backend.api.main import app as main_app

from asgi_lifespan import LifespanManager
from redis.asyncio import Redis


base_url = 'http://test'

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
        


GROUPS_INITIAL = { 
    "543": "1639", 
    "5413": "1638", 
    "543М": "1640",
    "5413М": "1634",
    "5423": "1638", 
}

