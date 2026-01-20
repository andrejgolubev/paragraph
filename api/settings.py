"""file with settings and configs for the backend"""
import logging
from pathlib import Path
from typing import Literal
from envparse import Env
from dotenv import load_dotenv
import os

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings

env = Env()
load_dotenv() 

BASE_DIR = Path(__file__).parent

DATABASE_URL = os.getenv('DATABASE_URL')
SECRET_KEY = os.getenv('SECRET_KEY')


LOG_DEFAULT_FORMAT = ("[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s")


class AuthJWT(BaseModel): 
    private_key_path: Path = BASE_DIR / 'certs' / 'jwt-private.pem' 
    public_key_path: Path = BASE_DIR / 'certs' / 'jwt-public.pem' 
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 30


class LoggingConfig(BaseModel): 
    log_level: Literal[
        "debug",
        "info",
        "warning",
        "error",
        "critical",
    ] = "info"
    log_format: str = LOG_DEFAULT_FORMAT

    @property
    def log_level_value(self) -> int:
        return logging.getLevelNamesMapping()[self.log_level.upper()]


class DatabaseConfig(BaseSettings): 
    # url: str = Field('DATABASE_URL', env='DATABASE_URL')
    url: str = DATABASE_URL
    future: bool = True
    echo: bool = False
    pool_size: int = 5
    max_overflow: int = 10


class CookiesConfig(BaseModel): 
    secure: bool = True  
    samesite: Literal['lax', 'samesite', 'none'] = 'lax'  


class RedisConfig(BaseModel): 
    schedule_cache_ttl: int = 60 * 5 # 5 minutes


class RateLimitSettings(BaseSettings):
    window_seconds: int = 5
    max_requests: int = 60
    cooldown_seconds: int = 60 * 5  # 5 min


class Settings(BaseSettings): 
    db: DatabaseConfig = DatabaseConfig()
    auth_jwt: AuthJWT = AuthJWT() 
    logging: LoggingConfig = LoggingConfig()
    cookie: CookiesConfig = CookiesConfig() 
    redis: RedisConfig = RedisConfig() 
    rate_limit: RateLimitSettings = RateLimitSettings()

    
settings = Settings()