from fastapi import Depends, HTTPException, Request, Response, status
import jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from ...core.config import settings
from ..auth import utils as auth_utils
from ..db.models import Group, User
from ..db.database import AsyncSessionLocal, get_db
from ..auth.helpers import get_refreshed_access_token


async def get_current_access_token_payload(
    request: Request,
    response: Response,
) -> dict:
    """Возвращает payload ТЕКУЩЕГО access-токена. Если access отсутствует 
    или истёк, пытается обновить его по refresh и, если успешно, то сразу 
    ставит полученный access_token в cookie."""

    unauth_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="пожалуйста, войдите в аккаунт.",
    )

    # refresh нет - значит время сессии истекло
    if not (refresh_token:= request.cookies.get("refresh_token")):
        raise unauth_exception


    # сначала пробуем действующий access
    if (access_token := request.cookies.get("access_token")):
        try:
            return auth_utils.decode_jwt(token=access_token)
        except jwt.exceptions.ExpiredSignatureError:
            # истёк — пойдём по refresh
            pass
        except jwt.exceptions.PyJWTError:
            raise unauth_exception

    # если access нет или истёк, пробуем refresh
    try:
        refresh_payload = auth_utils.decode_jwt(token=refresh_token)
    except jwt.exceptions.PyJWTError:
        raise unauth_exception

    try:
        async with AsyncSessionLocal() as session:
            new_access_token = await get_refreshed_access_token(
                payload=refresh_payload, db=session
            )
    except Exception:
        raise unauth_exception

    response.set_cookie(
        key="access_token",
        value=new_access_token,
        httponly=True,
        samesite=settings.cookie.samesite,  
        secure=True,  
        max_age=settings.auth_jwt.access_token_expire_minutes * 60,
    )

    # возвращаем payload от свежего access
    return auth_utils.decode_jwt(token=new_access_token)



async def get_current_auth_user(
    payload: dict = Depends(get_current_access_token_payload),
    db: AsyncSession = Depends(get_db),
) -> User:
    """Возвращает пользователя по access_token payload"""
    email: str = payload.get('sub')

    user_result = await db.scalars(select(User).where(User.email == email).options(
        selectinload(User.consents)
    ))

    if not (user:=user_result.first()):
        raise HTTPException(status_code=404, detail='Пользователь не найден')

    if not user.active: 
        raise HTTPException(status_code=403, detail='Отсутствуют необходимые права')

    
    return user
    
    

async def get_current_active_auth_user_data(
    user: User = Depends(get_current_auth_user),
    db: AsyncSession = Depends(get_db),
) -> dict:

    db_group = await db.scalars(select(Group).where(Group.id == user.group_id))

    if not (group := db_group.first()):
        group_number = None
    else: 
        group_number = group.group_number

    return {
        'id': user.id,
        "username": user.name,
        "email": user.email,
        "role": user.role,
        "group": group_number,  
        'consents': user.consents
    }


