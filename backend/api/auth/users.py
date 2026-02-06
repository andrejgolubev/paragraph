from fastapi import Body, Depends, HTTPException, Request, Response, status, APIRouter, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from random import choice
from pathlib import Path


from ..auth.validation import (
    get_current_active_auth_user_data,
)
from ..db.database import get_db
from ..db.models import Group, User, UserConsent
from ..db.schemas import UserRegistration, UserLogin, UserUpdate
from ...core.config import settings
from ..auth.utils import (
    hash_password,
    validate_password,
)
from .helpers import create_access_token, create_refresh_token
from .censor.censor import has_cursive_words
from ..utils.converters import latin_to_cyrillic
from ..logger import log


router = APIRouter(
    prefix="/user",
    tags=["user"],
)



def username_is_cyrillic_only(username: str) -> bool:
    allowed_chars = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя' + '-' + '.' + ' '
    return all(char.lower() in allowed_chars for char in username)


@router.post("/register")
async def register(
    request: Request,
    register_data: UserRegistration = Body(),
    db: AsyncSession = Depends(get_db),
):
    """для регистрации пользователя саморучно"""
    username = register_data.username
    email = register_data.email
    password = register_data.password
    group_number = register_data.group_number

    # ПРОВЕРКА ЧЕКБОКСОВ
    if not register_data.accept_pd:
        raise HTTPException(
            status_code=403, 
            detail="Необходимо дать согласие на обработку ПД",
        )
    
    if not register_data.accept_terms:
        raise HTTPException(
            status_code=403, 
            detail="Необходимо принять пользовательское соглашение и политику конфиденциальности",
        )


    if not username_is_cyrillic_only(username):
        raise HTTPException(status_code=400, detail="имя может содержать только кириллицу.")

    if await has_cursive_words(phrase=username): 
        answers: dict[str] = ['введённое имя недопустимо :(', 'такое имя неприемлимо :(', 'введённое имя не прошло валидацию :(']
        raise HTTPException(status_code=400, detail=choice(answers))    

    email_result = await db.scalars(select(User).where(User.email == email))
    
    if email_result.first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="пользователь с такой почтой уже существует.",
        )

    # серверная валидация группы, чтобы если пользователь не введет группу или введет что-то не то, 
    # то группа была null

    if not group_number:
        group_id = None
    else: 
        group_result = await db.scalars(
            select(Group).where(Group.group_number == latin_to_cyrillic(group_number))
        )
        if not (group := group_result.first()): 
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="группа не существует или введена не так, как на официальном сайте университета."
            )
        else: 
            group_id = group.id


    db_user = User(
        name=username,
        email=email,
        password=hash_password(password),
        role="student",
        active=True,
        group_id=group_id,  # будет None если группа не нашлась или не введена, и в БД будет null
    )

    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)

    ip = (
        request.headers.get("X-Forwarded-For", "").split(",")[0].strip()
        or request.headers.get("X-Real-IP")
        or (request.client.host if request.client else None)
    )

    pd_consent = UserConsent(
        user_id=db_user.id, 
        consent_type='pd',
        ip=ip
    )

    terms_consent = UserConsent(
        user_id=db_user.id, 
        consent_type='terms',
        ip=ip
    )
    db.add_all([terms_consent, pd_consent])

    await db.commit()

    log.info(
        'New user (%s) signed up!', 
        db_user_email:=db_user.email
    )

    return dict(
        id=db_user.id,
        name=db_user.name,
        email=db_user_email,
        role=db_user.role,
        active=db_user.active,
        group_id=db_user.group_id,
        detail='Вы успешно зарегистрировались!',
        status='ok'
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
            lifetime_seconds = settings.auth_jwt.access_token_expire_minutes*60 
        if key == 'refresh_token': 
            lifetime_seconds = settings.auth_jwt.refresh_token_expire_days*24*60*60
        response.set_cookie(
            key=key,
            value=value,
            httponly=True,
            samesite=settings.cookie.samesite,
            secure=True, 
            max_age=lifetime_seconds
        )   

    log.info(
        'User (%s , %s) signed in!', 
        user_name:=user.name, 
        user.email
    )
    
    return {
        "status": "ok",
        "detail": f"Вы вошли как {user.name}",
        'username': user_name,
        'role': user.role,
    }



@router.post('/logout') 
async def logout(response: Response): 
    response.delete_cookie(
        'access_token',
        samesite=settings.cookie.samesite, 
        httponly=True, 
        secure=True,
    )

    response.delete_cookie(
        'refresh_token', 
        samesite=settings.cookie.samesite, 
        httponly=True, 
        secure=True,
    )

    return {"status": "ok", "detail": "Вы вышли из аккаунта"}


@router.patch('/update-profile')
async def update_profile(
    current_user: dict = Depends(get_current_active_auth_user_data),
    update_data: UserUpdate = Body(),
    db: AsyncSession = Depends(get_db),
): 
    # только свой профиль
    if update_data.email != current_user.get("email"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="нельзя редактировать чужой профиль.",
        )
        
    if not (password:=update_data.password): 
        raise HTTPException(status_code=400, detail="для применения правок введите пароль.")

    if not username_is_cyrillic_only(username:=update_data.username):
        raise HTTPException(status_code=400, detail="имя может содержать только кириллицу.")

    if await has_cursive_words(phrase=username): 
        answers: dict[str] = [
            'введённое имя недопустимо :(', 
            'такое имя неприемлимо :(', 
            'введённое имя не прошло валидацию :('
        ]
        raise HTTPException(status_code=400, detail=choice(answers))  

    user_result = await db.scalars(select(User).where(User.email == update_data.email))
    user = user_result.first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="ошибка при обновлении данных: профиль не найден.",
        )
    
    if not validate_password(password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="введён неверный пароль",
        )
    

    if username:
        user.name = username
    if (group_number:=update_data.group_number):
        group_result = await db.scalars(select(Group).where(Group.group_number == latin_to_cyrillic(group_number)))
        group = group_result.first()
        if group:
            user.group_id = group.id
        else: 
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="группа не существует или введена не так, как на официальном сайте университета.",
            )
        

    db.add(user)
    await db.commit()
    await db.refresh(user)

    
    return {
        "status": "ok",
        "detail": "Профиль обновлен успешно",
        "username": user.name,
        "email": user.email,
        "role": user.role,
        "group": group.group_number if group_number else None,
    }


@router.get("/me")
def auth_user_check_self_info(user_data: dict = Depends(get_current_active_auth_user_data)):
    """Возвращает нечувствительные данные об авторизованном пользователе.
    Преимущественно для возрвата данных на фронтенд """

    return {
        "status": "ok",
        "username": user_data.get("username"),
        "email": user_data.get("email"),
        "role": user_data.get("role"),
        "group": user_data.get("group"),
    }


