import pytest
from httpx import AsyncClient, ASGITransport
from asgi_lifespan import LifespanManager  

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.main import app
from backend.api.db.models import User
from backend.api.schemas.users import UserRegistration, UserLogin, UserUpdate, RegistredUserResponse
from backend.api.auth.users import hash_password
from backend.tests.conftest import GROUPS_INITIAL, base_url


@pytest.mark.asyncio(loop_scope="session")
@pytest.mark.parametrize(
    "group, expected",
    [
        (None, 200),
        (" ", 404),
        ("164343", 404),
        ("5413M", 200), # латинская 
        ("5413М", 200), # кириллическая
        *[(group, 200) for group in GROUPS_INITIAL.keys()]
    ]
)
async def test_register(
    group: str, 
    expected: int, 
    db: AsyncSession, 
    clean_users  
):
    
    register_payload = UserRegistration(
        username="Иванов Иван",
        email="ivan@example.com",
        password="ComplexPass123!",
        group_number=group,
        accept_pd=True,
        accept_terms=True,
    ).model_dump()

    async with LifespanManager(app):
        async with AsyncClient(
            transport=ASGITransport(app=app), 
            base_url=base_url
        ) as client:
            response = await client.post("/user/register", json=register_payload)

    assert (status_code:=response.status_code) == expected

    if status_code == 200:
        user_result = await db.scalars(
            select(User).where(User.email == register_payload['email'])
        )
        assert (user := user_result.first()) is not None
        assert user.role == "student"



@pytest.mark.asyncio(loop_scope="session")
async def test_login(db: AsyncSession, clean_users):
    
    user = User(
        name="Иванов Иван",
        email="ivan@example.com",
        password=hash_password(test_password:='ComplexPass123!'),
        role="student",
        active=True,
        group_id=None,
    )
    db.add(user)
    await db.commit()

    login_payload = UserLogin(
        email=user.email,
        password=test_password,
    ).model_dump()

    async with LifespanManager(app):
        async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url=base_url,
        ) as client:
            response = await client.post("/user/login", json=login_payload)

    assert response.status_code == 200
    assert "access_token" in response.cookies
    assert "refresh_token" in response.cookies



@pytest.mark.asyncio(loop_scope="session")
async def test_logout(db: AsyncSession, clean_users):
    
    user = User(
        name="Иванов Иван",
        email="ivan@example.com",
        password=hash_password(test_password:='ComplexPass123!'),
        role="student",
        active=True,
        group_id=None,
    )
    db.add(user)
    await db.commit()

    login_payload = UserLogin(
        email=user.email,
        password=test_password,
    ).model_dump()

    async with LifespanManager(app):
        async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url=base_url,
        ) as client:
            login_response = await client.post("/user/login", json=login_payload)

            assert login_response.status_code == 200 
            assert "access_token" in login_response.cookies
            assert "refresh_token" in login_response.cookies
            logout_response = await client.post('/user/logout')


    assert logout_response.status_code == 200
    assert "access_token" not in logout_response.cookies
    assert "refresh_token" not in logout_response.cookies



@pytest.mark.asyncio(loop_scope="session")
@pytest.mark.parametrize("new_group, expected", [
    (None, 200),
    ("164343", 404),
    (" ", 404),
    *[(group, 200) for group in GROUPS_INITIAL.keys()]
])
async def test_update_profile(
    new_group: str, 
    expected: int, 
    db: AsyncSession, 
    clean_users
): 
    
    user = User(
        name="Иванов Иван",
        email="ivan@example.com",
        password=hash_password(test_password:='ComplexPass123!'),
        role="student",
        active=True,
        group_id=None,
    )
    db.add(user)
    await db.commit()

    login_payload = UserLogin(
        email=user.email,
        password=test_password,
    ).model_dump()

    update_payload = UserUpdate(
        username=(new_username:='Сергеев Сергей'),
        group_number=new_group,
        password=test_password,
    ).model_dump()

    async with LifespanManager(app):
        async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url=base_url,
        ) as client:
            login_response = await client.post("/user/login", json=login_payload)
            upd_response = await client.patch("/user/update-profile", json=update_payload)

    body = upd_response.json()
    if expected == 200: ...


    
    
