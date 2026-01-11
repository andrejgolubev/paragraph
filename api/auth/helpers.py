from datetime import timedelta

import jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.settings import settings
from api.auth import utils as auth_utils
from api.db.models import User

TOKEN_TYPE_FIELD = "type"
ACCESS_TOKEN_TYPE = "access"
REFRESH_TOKEN_TYPE = "refresh"


def create_jwt(
    payload: dict,
    token_type: str,
    expire_minutes: int = settings.auth_jwt.access_token_expire_minutes,
    expire_timedelta: timedelta | None = None,
) -> str:
    jwt_payload = {TOKEN_TYPE_FIELD: token_type}
    jwt_payload |= payload
    
    return auth_utils.encode_jwt(jwt_payload, expire_minutes=expire_minutes, expire_timedelta=expire_timedelta)



def create_access_token(payload: dict) -> str:
    return create_jwt(
        payload=payload,
        token_type=ACCESS_TOKEN_TYPE,
        expire_minutes=settings.auth_jwt.access_token_expire_minutes
    )


def create_refresh_token(payload: dict) -> str:
    return create_jwt(
        payload=payload,
        token_type=REFRESH_TOKEN_TYPE,
        expire_timedelta=timedelta(days=settings.auth_jwt.refresh_token_expire_days),
    )


async def get_refreshed_access_token(
    payload: dict,
    db: AsyncSession,
) -> str:
    """Выдаёт новый access-токен по действующему refresh payload."""
    credentials_exception = jwt.exceptions.PyJWTError("Время сессии истекло.")

    try:
        email: str = payload.get("sub")
        if not email:
            raise credentials_exception
    except Exception:
        raise credentials_exception

    user_result = await db.scalars(select(User).where(User.email == email))
    user = user_result.first()

    if not user or not user.active:
        raise credentials_exception

    return auth_utils.encode_jwt(
        payload={
            "sub": user.email,
            "role": user.role,
            "username": user.name,
        }
    )

