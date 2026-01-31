import pytest
from httpx import AsyncClient, ASGITransport
from asgi_lifespan import LifespanManager  

from sqlalchemy import select, delete

from backend.api.db.database import AsyncSessionLocal
from backend.api.main import app
from backend.core.config import settings
from backend.api.db.models import User
from backend.api.db.schemas import UserRegistration, UserLogin
from backend.api.auth.users import hash_password


@pytest.mark.asyncio(loop_scope="session")
async def test_register():
    # Подготовка данных — отдельная сессия
    async with AsyncSessionLocal() as db:
        await db.execute(delete(User))
        await db.commit()
    
    payload = UserRegistration(
        username="Иванов Иван",
        email="ivan@example.com",
        password="ComplexPass123!",
        group_number=None,
        accept_pd=True,
        accept_terms=True,
    ).model_dump()

    async with LifespanManager(app):
        async with AsyncClient(
            transport=ASGITransport(app=app), 
            base_url=settings.url.https
        ) as client:
            response = await client.post("/user/register", json=payload)

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["email"] == payload["email"]

    # Проверка в БД — отдельная сессия
    async with AsyncSessionLocal() as db:
        user_result = await db.scalars(
            select(User).where(User.email == payload["email"])
        )
        assert (user := user_result.first()) is not None
        assert user.role == "student"


@pytest.mark.asyncio(loop_scope="session")
async def test_login():
    test_password = "ComplexPass123!"
    
    # Подготовка данных — отдельная сессия
    async with AsyncSessionLocal() as db:
        await db.execute(delete(User))
        await db.commit()
        
        user = User(
            name="Тест Юзер",
            email="login@example.com",
            password=hash_password(test_password),
            role="student",
            active=True,
            group_id=None,
        )
        db.add(user)
        await db.commit()
        user_email = user.email

    login_payload = UserLogin(
        email=user_email,
        password=test_password,
    ).model_dump()

    async with LifespanManager(app):
        async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url=settings.url.https,
        ) as client:
            response = await client.post("/user/login", json=login_payload)

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert "access_token" in response.cookies
    assert "refresh_token" in response.cookies