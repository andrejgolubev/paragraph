from fastapi import Depends, Form, HTTPException, Request, status
import jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN

from api.db.models import Group, User

from .validation import get_current_auth_user
from api.db.database import get_db
from api.auth import utils as auth_utils


async def validate_auth_user( # ФУНКЦИЯ ПЕРЕЕХАЛА CМОТРИ users.py / router.post('/login')
    email: str = Form(), 
    password: str = Form(), 
    db: AsyncSession = Depends(get_db),
):
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="неверный логин или пароль"
    )

    user_result = await db.scalars(select(User).where(User.email == email))
    user = user_result.first()
    if not user:
        raise unauthed_exc

    if not auth_utils.validate_password(
        password=password, hashed_password=user.password
    ):
        raise unauthed_exc

    if not user.active:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="доступ запрещен")

    return user





async def get_current_active_auth_user(
    user: User = Depends(get_current_auth_user),
    db: AsyncSession = Depends(get_db),
):
    db_group = await db.scalars(select(Group).where(Group.id == user.group_id))

    if not (group_number := db_group.first().group_number):
        group_number = ""

    return {
        "username": user.name,
        "email": user.email,
        "role": user.role,
        "group": group_number,  # слева будет None если группа не указана, так что
    }


async def get_current_admin(
    user: User = Depends(get_current_active_auth_user),
):
    if "admin" in user.role and user.group:
        ...



