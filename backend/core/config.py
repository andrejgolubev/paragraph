"""file with settings and configs for the backend"""
import logging
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).parent.parent

LOG_DEFAULT_FORMAT = ("[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s")


class AuthJWT(BaseModel): 
    private_key_path: Path = BASE_DIR / 'api' / 'certs' / 'jwt-private.pem' 
    public_key_path: Path = BASE_DIR / 'api' / 'certs' / 'jwt-public.pem' 
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
    ] = "debug"
    log_format: str = LOG_DEFAULT_FORMAT

    @property
    def log_level_value(self) -> int:
        # DEBUG -> 10 , INFO -> 20 , ...
        return logging.getLevelNamesMapping()[self.log_level.upper()]


class DatabaseConfig(BaseSettings): 
    scheme: str = Field('postgresql+asyncpg', env='DB__URL')
    user: str = Field('pg', env="DB__USER")
    password: str = Field('root', env="DB__PASSWORD")
    host: str = Field('localhost', env="DB__HOST")
    port: int = Field(5433, env="DB__PORT")
    name: str = Field('pg', env="DB__NAME")

    future: bool = True
    echo: bool = False
    pool_size: int = 5 # prod:10
    max_overflow: int = 10 # prod:20


class CookiesConfig(BaseModel): 
    secure: bool = True  
    samesite: Literal['lax', 'samesite', 'none'] = 'lax'  


class RedisConfig(BaseModel): 
    host: str = Field('localhost', env='REDIS__HOST')
    port: int = Field(6380, env='REDIS__HOST')
    password: str = Field('root', env='REDIS__PASSWORD')
    db: int = Field(0, env='REDIS__DB')
    schedule_cache_ttl: int = 60 * 5 # 5 minutes


class RateLimitConfig(BaseModel):
    window_seconds: int = 5
    max_requests: int = 80
    cooldown_seconds: int = 60 * 5  # 5 min



class Settings(BaseSettings): 
    model_config = SettingsConfigDict(
        env_file=(
            BASE_DIR / ".env",
            BASE_DIR / ".env.prod",
        ),
        env_nested_delimiter='__',
        case_sensitive=False,
        extra='ignore' 
    )

    db: DatabaseConfig = DatabaseConfig()
    auth_jwt: AuthJWT = AuthJWT() 
    logging: LoggingConfig = LoggingConfig()
    cookie: CookiesConfig = CookiesConfig() 
    redis: RedisConfig = RedisConfig() 
    rate_limit: RateLimitConfig = RateLimitConfig()

    
settings = Settings() 



