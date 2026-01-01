from fastapi import Depends, HTTPException, Request, status
import jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from api.auth import utils as auth_utils
from api.db.models import Group, User
from api.db.database import get_db


def get_access_token_payload(
    request: Request,
) -> dict:
    
    unauth_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="пожалуйста, войдите в аккаунт.",
    )
    try:
        if not (token := request.cookies.get("access_token")):
            raise unauth_exception
        payload = auth_utils.decode_jwt(token=token)

    except jwt.exceptions.PyJWTError:
        raise unauth_exception

    return payload

def get_refresh_token_payload(
    request: Request,
) -> dict:
    
    unauth_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="время сессии истекло.",
    ) # чисто для swagger UI. в middleware отлавливается 

    try:
        if not (token := request.cookies.get("refresh_token")):
            raise unauth_exception
        payload = auth_utils.decode_jwt(token=token)

    except jwt.exceptions.PyJWTError:
        raise unauth_exception

    return payload



async def get_current_auth_user(
    payload: dict = Depends(get_access_token_payload),
    db: AsyncSession = Depends(get_db),
) -> User:
    """returns user by payload NO MATTER HE IS ACTIVE OR NOT 
    (should not be used as dependency, 
    better use get_current_active_auth_user)"""
    email: str = payload.get('sub')

    user_result = await db.scalars(select(User).where(User.email == email))

    if not (user := user_result.first()): 
        raise HTTPException(status_code=404, detail='user not found')

    if not user.active: 
        raise HTTPException(status_code=403, detail='user inactive ')
        
        
    return user
    
    

async def get_current_active_auth_user(
    user: User = Depends(get_current_auth_user),
    db: AsyncSession = Depends(get_db),
) -> dict:
    db_group = await db.scalars(select(Group).where(Group.id == user.group_id))

    if not (group_number := db_group.first().group_number):
        group_number = ""

    return {
        "username": user.name,
        "email": user.email,
        "role": user.role,
        "group": group_number,  # слева будет None если группа не указана, так что
    }

