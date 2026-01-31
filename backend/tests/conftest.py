import pytest, subprocess

from backend.api.auth.helpers import create_access_token, create_refresh_token
from backend.core.config import settings
from backend.api.db.database import AsyncSessionLocal

@pytest.fixture(scope='session', autouse=True)
def storage_setup():
    """
    Проверяет, подставляются ли перезаписывающие тестовые переменные окружения
    из .env.test из корня проекта и подгатавливает хранилища к работе
    """
    assert settings.db.port == 5435  
    assert settings.redis.port == 6381  
    subprocess.run(["poetry", "run", "alembic", "upgrade", "head"], check=True)


@pytest.fixture(scope='function')
async def db(): 
    async with AsyncSessionLocal() as session:
        yield session


# @pytest.fixture(scope='session', autouse=True)
# def get_current_user_tokens():
#     """Возвращает токены абстрактного пользователя"""

#     access_token = create_access_token(
#         payload= (sub:={"sub": "user@example.com"}) | {"role": "student", "username": "Олег"} 
#     )

#     refresh_token = create_refresh_token(payload=sub)

#     return {
#         'access_token': access_token,
#         'refresh_token': refresh_token,
#     }