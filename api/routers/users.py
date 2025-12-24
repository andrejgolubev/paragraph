from fastapi import Depends, HTTPException, status, APIRouter, Query
from api.db.database import get_db
from api.db.models import User
from api.db.schemas import UserResponse, UserRegistration
from sqlalchemy import select
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from api.routers.auth import (
    create_access_token,
    create_refresh_token,
    verify_password,
    hash_password,
    verify_admin_api_key,
)
import jwt
import settings

user_router = APIRouter()
security = HTTPBasic()


@user_router.post("/register/", response_model=UserResponse)
async def register(user: UserRegistration, db: AsyncSession = Depends(get_db)):
    """для регистрации пользователя саморучно. использует UserRegistration, наследующую от UserCreate.
    не имеет функц. задавать role, rating."""

    result = await db.scalars(select(User).where(User.name == user.name))
    existing_user = result.first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с таким именем уже существует.",
        )

    user.password = hash_password(user.password)

    db_user = User(**user.model_dump())
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)

    return db_user


@user_router.post("/make-admin/", dependencies=[Depends(verify_admin_api_key)])
async def make_admin(
    username: str = Query(alias="who to make an admin?"),
    admin_type: str = Query(alias="For example: admin543, adminКрасноеЗнамя"),
    db: AsyncSession = Depends(get_db),
):
    """делает админом :O   (или наоборот)"""

    user = await db.scalars(select(User).where(User.name == username))
    user = user.first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="пользователя с таким именем не существует.",
        )

    user.role = admin_type

    db.add(user)
    await db.commit()
    await db.refresh(user)

    return {
        "message": f"{user.name}`s role got updated.",
        "username": user.name,
        "role": user.role,
    }


# -------------------------------------------------------------AUTH OPERATIONS-------------------------------------------------------------


@user_router.post("/login", name="login")
async def login(
    form_data: HTTPBasicCredentials = Depends(security),
    db: AsyncSession = Depends(get_db),
):
    """
    Аутентифицирует пользователя и возвращает access_token и refresh_token.
    create_access_token и create_refresh_token создают JWT-токены
    с одинаковым payload (sub, role, id), но разным временем истечения (exp)
    """
    result = await db.scalars(select(User).where(User.name == form_data.username))
    user = result.first()
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect nickname or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        data={"sub": user.name, "role": user.role, "id": user.id}
    )
    refresh_token = create_refresh_token(
        data={"sub": user.name, "role": user.role, "id": user.id}
    )

    return {
        "username": user.name,
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@user_router.get("/get-role", name="role")
async def get_user_role(username: str, db: AsyncSession = Depends(get_db)):
    """получает роль : студент или админ"""
    user = await db.scalars(select(User).where(User.name == username))
    user_first = user.first()
    if not user_first:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="username doesn`t exist"
        )
    role = user_first.role  # type:ignore
    group = 'unknown'

    if "admin" in role:
        group = role[role.index("admin") + 5 :]
        role = "admin"

    return {"role": role, "group": group}


@user_router.post("/refresh-token")
async def refresh_token(refresh_token: str, db: AsyncSession = Depends(get_db)):
    """
    Обновляет access_token с помощью refresh_token.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate refresh token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            refresh_token, settings.SECRET_KEY or "", algorithms=[settings.ALGORITHM]
        )
        # Автоматически проверяется exp! Если токен просрочен, здесь выбросится исключение.
        name: str = payload.get("sub")
        if not name:
            raise credentials_exception
    except jwt.exceptions:
        raise credentials_exception
    result = await db.scalars(select(User).where(User.name == name))
    user = result.first()
    if not user:
        raise credentials_exception
    access_token = create_access_token(
        data={
            "sub": user.name,
            "role": user.role,
            "id": user.id,
        }
    )
    return {"access_token": access_token, "token_type": "bearer"}
