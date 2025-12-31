import jwt
from api.settings import settings
import bcrypt
from datetime import UTC, datetime, timedelta 
from fastapi import HTTPException, status, Header
import os


def encode_jwt(
    payload: dict,
    private_key: str = settings.auth_jwt.private_key_path.read_text(),
    algorithm: str = settings.auth_jwt.algorithm,
    expire_minutes: int = settings.auth_jwt.access_token_expire_minutes,
    expire_timedelta: timedelta|None = None,
):

    now = datetime.now(tz=UTC)
    expire = now + expire_timedelta if expire_timedelta else now + timedelta(minutes=expire_minutes)
    payload |= {
        'exp': expire, 
        'iat': now,
    }

    return jwt.encode(payload, private_key, algorithm)


def decode_jwt(
    token: str | bytes,
    public_key: str = settings.auth_jwt.public_key_path.read_text(),
    algorithm: str = settings.auth_jwt.algorithm,
):

    return jwt.decode(token, public_key, algorithms=[algorithm])


def hash_password(password: str) -> bytes:
    salt = bcrypt.gensalt()
    pwd_bytes: bytes = password.encode('utf-8')
    return bcrypt.hashpw(pwd_bytes, salt).decode('utf-8')


def validate_password(
    password: str,
    hashed_password: str,
) -> bool:
    return bcrypt.checkpw(
        password=password.encode('utf-8'),
        hashed_password=hashed_password.encode('utf-8'),
    )




API_KEY = os.getenv("ADMIN_API_KEY", 'secret-key')

async def verify_admin_api_key(api_key: str = Header(alias="API-Key")):
    if api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API Key"
        )