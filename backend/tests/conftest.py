import pytest, subprocess

from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.db.models import User
from backend.core.config import settings
from backend.api.db.database import AsyncSessionLocal


@pytest.fixture(scope='session', autouse=True)
def storage_setup():
    """
    Проверяет, перезаписываются ли переменные окружения на тестовые
    из .env.test из корня проекта и подгатавливает хранилища к работе
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
    """для очистки таблицы users перед и после тестов"""
    await db.execute(delete(User))
    await db.commit()
    yield
    await db.execute(delete(User))
    await db.commit()


groups_initial = { 
    "543": "1639", 
    "5413": "1638", 
    "543М": "1640",
    "5413М": "1634",
    "5423": "1638", 
}