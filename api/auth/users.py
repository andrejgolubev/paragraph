import jwt
from api.auth.validation import get_current_active_auth_user
from api.auth.validation import get_access_token_payload, get_refresh_token_payload
from api.db.database import get_db
from api.db.models import Group, User
from api.db.schemas import UserRegistration, UserLogin
from api import settings
from api.auth.utils import (
    encode_jwt,
    hash_password,
    validate_password,
    verify_admin_api_key,
)

from fastapi import Body, Depends, Form, HTTPException, Response, status, APIRouter, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from .helpers import create_access_token, create_refresh_token

router = APIRouter(
    prefix="/user",
    tags=["user"],
)


@router.post("/register")
async def register(
    register_data: UserRegistration = Body(),
    db: AsyncSession = Depends(get_db),
):
    """для регистрации пользователя саморучно"""
    username = register_data.username
    email = register_data.email
    password = register_data.password
    group_number = register_data.group_number

    result = await db.scalars(select(User).where(User.email == email))

    if result.first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="пользователь с такой почтой уже существует.",
        )

    group_result = await db.scalars(
        select(Group).where(Group.group_number == group_number)
    )

    db_user = User(
        name=username,
        email=email,
        password=hash_password(password),
        role="student",
        active=True,
        group_id=group_result.first().id,  # будет None если группа не нашлась и в БД будет null
    )

    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)

    return dict(
        id=db_user.id,
        name=db_user.name,
        email=db_user.email,
        role=db_user.role,
        active=db_user.active,
        group_id=db_user.group_id,
    )


@router.post("/login", name="login")
async def login(
    response: Response,
    login_data: UserLogin = Body(),
    db: AsyncSession = Depends(get_db),
):  

    email = login_data.email
    password = login_data.password

    result = await db.scalars(select(User).where(User.email == email))
    if not (user := result.first()) or not validate_password(password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="неверный email или пароль",
        )

    if not user.active:
        raise HTTPException(
            status_code=403,
            detail="доступ запрещён",
        )

    access_token = create_access_token(
        payload={"sub": user.email, "role": user.role, "username": user.name}
    )

    refresh_token = create_refresh_token(payload={"sub": user.email})

    secure_cookies = {
        'access_token': access_token, 
        'refresh_token': refresh_token,
    }
    for key, value in secure_cookies.items():
        if key == 'access_token': 
            lifetime_seconds = settings.settings.auth_jwt.access_token_expire_minutes*60 
        if key == 'refresh_token': 
            lifetime_seconds = settings.settings.auth_jwt.refresh_token_expire_days*24*60*60
        response.set_cookie(
            key=key,
            value=value,
            httponly=True,
            secure=True,  # только для htpps
            samesite="none",  
            max_age=lifetime_seconds
        )   

    

    return {
        "message": "успешный вход",
        "access": access_token, 
        "refresh": refresh_token
    }


@router.post("/make-admin/", dependencies=[Depends(verify_admin_api_key)])
async def make_admin(
    email: str = Query(alias="почта того, кого сделать админом"),
    groups_to_admin: str = Query(
        alias="Например: 543, 5413. Можно указать несколько через запятую."
    ),
    db: AsyncSession = Depends(get_db),
):
    """делает админом :O"""

    user_result = await db.scalars(select(User).where(User.email == email))
    user = user_result.first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="пользователя с такой почтой не существует.",
        )

    user.role = "admin." + ".".join(set(
        [gr.strip() for gr in groups_to_admin.split(",")]
    ))

    db.add(user)
    await db.commit()
    await db.refresh(user)

    return {
        "message": f"{user.name}`s role is now: {user.role}",
        "role": user.role,
    }


@router.get("/me")
def auth_user_check_self_info(user: dict = Depends(get_current_active_auth_user)):
    """для возрвата данных на фронтенд в раздел 'профиль'"""
    return {
        "username": user.get("username"),
        "email": user.get("email"),
        "role": user.get("role"),
        "group": user.get("group"),
    }





async def get_refreshed_access_token(
    payload: dict = Depends(get_refresh_token_payload),
    db: AsyncSession = Depends(get_db), 

):  
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate refresh token",
    )
    try:
        # автоматически проверяется exp и если токен просрочен, здесь выбросится исключение.
        email: str = payload.get("sub")
        if not email:
            raise credentials_exception
    except jwt.exceptions.PyJWTError:
        raise credentials_exception
    user_result = await db.scalars(select(User).where(User.email == email))
    user = user_result.first()
    if not user:
        raise credentials_exception

    access_token = encode_jwt(
        payload={
            "sub": user.email,
            "role": user.role,
            "username": user.name,
        }
    )

    return access_token

    


@router.post("/refresh-token")
async def refresh_token(
    response: Response,
    payload: dict = Depends(get_refresh_token_payload), 
    db: AsyncSession = Depends(get_db)):
    """
    Обновляет access_token с помощью refresh_token.
    """

    access_token = await get_refreshed_access_token(payload=payload, db=db)

    response.set_cookie(
            key='access_token',
            value=access_token,
            httponly=True,
            secure=True,  # для htpps
            samesite="none",  
            max_age=settings.settings.auth_jwt.access_token_expire_minutes*60
        )  

    return {"message": 'токен успешно обновлен'}
