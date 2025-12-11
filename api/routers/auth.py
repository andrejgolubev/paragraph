import jwt.exceptions
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta, timezone
import jwt
from fastapi import Depends, HTTPException, status, Header
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import bcrypt
from api.db.models import User as UserModel
from settings import SECRET_KEY, ALGORITHM
from api.db.database import get_db
import os
# Создаём контекст для хеширования с использованием bcrypt

ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7 

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/token", auto_error=False) 
#"users/token" это ПУТЬ К ЭНДПОИНТУ (роутеру в нашем случае) в app.routers.users с этим url 
# Создает кнопку "Authorize" в Swagger UI
# Показывает куда отправлять запрос для получения токена
# Автоматически добавляет security scheme в OpenAPI спецификацию

# Получаем ключ из переменных окружения
API_KEY = os.getenv("ADMIN_API_KEY", 'secret-key')

async def verify_admin_api_key(api_key: str = Header(alias="API-Key")):
    if api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API Key"
        )


def hash_password(password: str) -> str:

    '''Преобразует пароль в хеш с использованием bcrypt.'''
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode(encoding='utf-8')

    
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверяет, соответствует ли введённый пароль сохранённому хешу."""

    return bcrypt.checkpw(password=plain_password.encode(), hashed_password=hashed_password.encode())




def create_refresh_token(data: dict):          # New
    """
    Создаёт рефреш-токен с payload (sub, role, id, exp).
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM) #type: ignore


def create_access_token(data: dict): 
    """
    Создаёт JWT с payload (sub, role, id, exp).
    в data подаётся словарь в ручке из users.py с данными.
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM) #type: ignore


async def get_current_user(token: str = Depends(oauth2_scheme),
                           db: AsyncSession = Depends(get_db)):
    """
    Проверяет JWT и возвращает пользователя из базы.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])  #type: ignore
        name: str = payload.get("sub")
        
        if not name:
            raise credentials_exception
    except jwt.exceptions:
        raise credentials_exception
    result = await db.scalars(
        select(UserModel).where(UserModel.name == name))
    user = result.first()
    if not user:
        raise credentials_exception
    return user 


async def get_current_admin(current_user: UserModel = Depends(get_current_user)):
    """
    Проверяет, что пользователь имеет роль 'admin'.
    """
    if current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins can perform this action")
    return current_user

