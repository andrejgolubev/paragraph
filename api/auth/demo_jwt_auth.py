from fastapi import (APIRouter, Depends, Form, HTTPException, status)
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN

from api.db.models import Group, User

from fastapi.security import OAuth2PasswordBearer, HTTPAuthorizationCredentials, HTTPBearer
from api.db.database import get_db
from api.db.schemas import TokenInfo
from api.auth import utils as auth_utils
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError

router = APIRouter(prefix='/jwt', tags=['JWT'])

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/jwt/login", 
    scheme_name="EmailPassword"
)

http_bearer = HTTPBearer()


async def validate_auth_user(
    email: str = Form(),
    password: str = Form(),
    db: AsyncSession = Depends(get_db)
): 
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='неверный логин или пароль')

    user_result = await db.scalars(select(User).where(User.email == email))
    user = user_result.first()
    if not user:
        raise unauthed_exc 
    
    if not auth_utils.validate_password(
        password=password,
        hashed_password=user.password
    ): 
        raise unauthed_exc

    if not user.active: 
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, 
            detail='доступ запрещен'
        ) 
    
    return user
    
def get_current_token_payload(
    creds: HTTPAuthorizationCredentials = Depends(http_bearer),
) -> User: 
    try:
        payload = auth_utils.decode_jwt(
            token=creds.credentials
        )
    except Exception as e: 
        raise HTTPException(status_code= HTTP_401_UNAUTHORIZED,
         detail=f"пожалуйста, войдите в аккаунт.")
    


    return payload



async def get_current_auth_user(
    payload: dict = Depends(get_current_token_payload),
    db: AsyncSession = Depends(get_db),
) -> User:
    """returns user by payload NO MATTER IF HE IS ACTIVE OR NOT"""
    email: str = payload.get('sub') 
    db_user = await db.scalars(select(User).where(User.email == email))
    if not (user:=db_user.first()): 
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="token invalid") 
    

    return user

async def get_current_active_auth_user(
    user: User = Depends(get_current_auth_user),
    db: AsyncSession = Depends(get_db),
): 
    db_group = await db.scalars(select(Group).where(Group.id == user.group_id))

    if not (group_number := db_group.first().group_number): group_number = ""

    return {
        "username": user.name,
        "email": user.email, 
        "role": user.role,
        "group": group_number # слева будет None если группа не указана, так что 
    }

async def get_current_admin(
    user: User = Depends(get_current_active_auth_user),
): 
    if 'admin' in user.role and user.group: 
        ...


@router.post('/login', response_model = TokenInfo)
def auth_user_issue_jwt(
    user: User = Depends(validate_auth_user),
): 

    payload = {
        'username': user.name,
        'sub': user.email, 
    }

    # собираем токен с username, sub, exp и iat
    access_token = auth_utils.encode_jwt(payload) 

    return TokenInfo(
        access_token=access_token, 
        token_type='Bearer'
    )


@router.get('/users/me')
def auth_user_check_self_info(
    user: dict = Depends(get_current_active_auth_user)
): 
    return {
        'username': user.get('username'), 
        'email': user.get('email'), 
        'role': user.get('role'),
        "group": user.get('group')
    }
