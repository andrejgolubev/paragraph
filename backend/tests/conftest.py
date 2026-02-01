import pytest, subprocess

from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.db.models import User
from backend.core.config import settings
from backend.api.db.database import AsyncSessionLocal
from backend.api.main import app as main_app

from asgi_lifespan import LifespanManager
from redis.asyncio import Redis


@pytest.fixture(scope='session', autouse=True)
def storage_setup():
    """
    Проверяет, перезаписываются ли переменные окружения на тестовые
    из .env.test из корня проекта и накатывает миграции в БД.

    Важно:
    Если на соответствующих портах не запущены тестовые хранилища - 
    все тесты упадут, т.к. используется autouse=True. 
    Также тесты упадут, если запускать `pytest` не из директории backend
    """
    assert settings.db.port == 5435  
    assert settings.redis.port == 6381  
    subprocess.check_call(["poetry", "run", "alembic", "upgrade", "head"])


@pytest.fixture
async def db(): 
    async with AsyncSessionLocal() as session:
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
        return redis



GROUPS_INITIAL = { 
    "543": "1639", 
    "5413": "1638", 
    "543М": "1640",
    "5413М": "1634",
    "5423": "1638", 
}