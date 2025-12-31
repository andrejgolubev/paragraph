"""File with settings and configs for the project"""
from pathlib import Path
from envparse import Env
from dotenv import load_dotenv
import os

from pydantic import BaseModel

env = Env()

BASE_DIR = Path(__file__).parent

DATABASE_URL = env.str(
    "DATABASE_URL",
    default="postgresql+asyncpg://postgres:root@127.0.0.1:5433/postgres"
)  # connect string for the database


load_dotenv() 
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = "RS256"


class AuthJWT(BaseModel): 
    private_key_path: Path = BASE_DIR / 'certs' / 'jwt-private.pem' 
    public_key_path: Path = BASE_DIR / 'certs' / 'jwt-public.pem' 
    algorithm: str = ALGORITHM
    access_token_expire_minutes: int = 1
    refresh_token_expire_days: int = 30


class Settings: 
    db_url: str = DATABASE_URL
    auth_jwt: AuthJWT = AuthJWT() 

    
settings = Settings()