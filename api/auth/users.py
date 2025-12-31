from api.auth.demo_jwt_auth import get_current_active_auth_user
from api.db.database import get_db
from api.db.models import Group, User
from api.db.schemas import UserResponse
from api import settings
from api.auth.utils import encode_jwt, hash_password, validate_password, verify_admin_api_key

from fastapi import Depends, Form, HTTPException, Response, status, APIRouter, Query
from fastapi.security import (
    HTTPBasicCredentials,
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
)
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import jwt

user_router = APIRouter()


@user_router.post("/register", response_model=UserResponse)
async def register(
    username: str = Form(),
    email: str = Form(),
    password: str = Form(),
    group_number: str = Form(),
    db: AsyncSession = Depends(get_db),
):
    """для регистрации пользователя саморучно"""

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


@user_router.post("/make-admin/", dependencies=[Depends(verify_admin_api_key)])
async def make_admin(
    response: Response,
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

@user_router.get('/me')
def auth_user_check_self_info(
    user: dict = Depends(get_current_active_auth_user)
): 
    return {
        'username': user.get('username'), 
        'email': user.get('email'), 
        'role': user.get('role'),
        "group": user.get('group')
    }

# -------------------------------------------------------------AUTH OPERATIONS-------------------------------------------------------------


@user_router.post("/login", name="login")
async def login(
    response: Response,
    email: str = Form(),
    password: str = Form(),
    db: AsyncSession = Depends(get_db),
):

    result = await db.scalars(select(User).where(User.email == email))
    if not (user := result.first()) or not validate_password(password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="неверный email или пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = encode_jwt(
        payload={"sub": user.email, "role": user.role, "username": user.name}
    )

    response.set_cookie(
        key="access_token",
        value=access_token, 
        httponly=True,
        secure=True, # только для htpps 
        samesite='strict' # защита от csrf 
    )

    return {
        "username": user.name,
        "access_token": access_token,
        # "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@user_router.get("/get-role", name="role")
async def get_user_role(username: str, db: AsyncSession = Depends(get_db)):
    db_user = await db.scalars(select(User).where(User.name == username))
    if not (user := db_user.first()):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="username doesn`t exist"
        )

    return {"role": user.role}


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
            refresh_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        # Автоматически проверяется exp! Если токен просрочен, здесь выбросится исключение.
        email: str = payload.get("sub")
        if not email:
            raise credentials_exception
    except jwt.exceptions:
        raise credentials_exception
    result = await db.scalars(select(User).where(User.email == email))
    user = result.first()
    if not user:
        raise credentials_exception
    access_token = encode_jwt(
        data={
            "sub": user.email,
            "role": user.role,
            "id": user.id,
        }
    )
    return {"access_token": access_token, "token_type": "bearer"}
