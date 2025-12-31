from fastapi import Depends, HTTPException, Request, status
import jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


from api.auth import utils as auth_utils
from api.auth.helpers import ACCESS_TOKEN_TYPE, REFRESH_TOKEN_TYPE, TOKEN_TYPE_FIELD
from api.db.models import User

from api.db.database import get_db


def get_current_token_payload(
    request: Request,
) -> dict:
    unauth_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="пожалуйста, войдите в аккаунт.",
    )
    try:
        if not (access_token := request.cookies.get("access_token")):
            if not (refresh_token := request.cookies.get('refresh_token')): 
                raise unauth_exception
            else: 
                payload = auth_utils.decode_jwt(token=refresh_token)
        else: 
            payload = auth_utils.decode_jwt(token=access_token)

    except jwt.exceptions.PyJWTError as e:
        raise unauth_exception

    return payload




def validate_token_type(
    payload: dict,
    token_type: str,
) -> bool:
    current_token_type = payload.get(TOKEN_TYPE_FIELD)
    if current_token_type == token_type: 
        return True 
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, 
        detail = f"неверный тип токена {current_token_type!r}, ожидался {token_type!r}", )


async def get_user_by_token_sub(
    payload: dict, 
    db: AsyncSession, 
) -> User: 
    email: str = payload.get("sub")
    db_user = await db.scalars(select(User).where(User.email == email)) 
    if not (user := db_user.first()):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="token invalid"
        )

    return user


def get_auth_user_from_token_of_type(
    token_type: str, 
    # db: AsyncSession = Depends(get_db)
): 
    async def get_auth_user_from_token(
        payload: dict = Depends(get_current_token_payload), 
        db: AsyncSession = Depends(get_db)
    ) -> User:
        if validate_token_type(payload, token_type):
            return await get_user_by_token_sub(payload, db=db)

    return get_auth_user_from_token


async def get_current_auth_user(
    payload: dict = Depends(get_auth_user_from_token_of_type(ACCESS_TOKEN_TYPE)),
    db: AsyncSession = Depends(get_db),
) -> User:
    """returns user by payload NO MATTER IF HE IS ACTIVE OR NOT"""
    return get_user_by_token_sub(payload, db=db)
    
    


async def get_current_auth_user_for_refresh(
    payload: dict = Depends(get_auth_user_from_token_of_type(REFRESH_TOKEN_TYPE)),
    db: AsyncSession = Depends(get_db),
) -> User:

    if validate_token_type(payload, REFRESH_TOKEN_TYPE):
        return get_user_by_token_sub(payload, db=db)
