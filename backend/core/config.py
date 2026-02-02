"""file with settings and configs for the backend"""
import logging
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).parent.parent
ROOT_DIR = BASE_DIR.parent

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
    ] = "info"
    log_format: str = LOG_DEFAULT_FORMAT
    max_file_size_mb: int = 5
    backup_files: int = 3

    @property
    def log_level_value(self) -> int:
        """DEBUG -> 10 , INFO -> 20 , ..."""
        return logging.getLevelNamesMapping()[self.log_level.upper()]


class DatabaseConfig(BaseSettings): 
    scheme: str = Field('postgresql+asyncpg')
    user: str = Field('pg')
    password: str = Field('root')
    host: str = Field('localhost')
    port: int = Field(5435)
    name: str = Field('pg')

    @property
    def url(self):
        return (
            f"{self.scheme}://{self.user}:{self.password}"
            f"@{self.host}:{self.port}/{self.name}"
        )
    
    @property
    def test_url(self):
        return (
            f"{self.scheme}://{self.user}:{self.password}"
            f"@{self.host}:{self.port + 1}/{self.name}"
        )

    future: bool = True
    echo: bool = False
    pool_size: int = 5 # prod:10
    max_overflow: int = 10 # prod:20


class CookiesConfig(BaseModel): 
    secure: bool = True  
    samesite: Literal['lax', 'samesite', 'none'] = 'none'  


class RedisConfig(BaseModel): 
    host: str = Field('localhost')
    port: int = Field(6381)
    password: str = Field('root')
    db: int = Field(0)
    schedule_cache_ttl: int = 60 * 5 # 5 minutes

    @property
    def url(self): 
        return (
            f"redis://:{self.password}@{self.host}:{self.port}/{self.db}"
        )

    @property
    def test_url(self): 
        return (
            f"redis://:{self.password}@{self.host}:{self.port + 1}/{self.db}"
        )


class RateLimitConfig(BaseModel):
    window_seconds: int = 5
    max_requests: int = 80
    cooldown_seconds: int = 60 * 5  # 5 min


class AdminConfig(BaseModel): 
    api_key: str = Field('super_secret_key')


class DocsConfig(BaseModel): 
    enabled: bool = Field(True) # Pydantic приводит к bool env value


class AppConfig(BaseModel): 
    """
    1. Если dev=True, то: 
    - используются локальные Postgres и Redis (на порте +1) для тестирования
    - "https://localhost:8000" - по такой ссылке ходит фронтенд к API 


    2. Также можно в ./frontend/.env установить APP__LOCAL_NGINX=true ,
    чтобы использовать локальный реверс-прокси сервер nginx, конфигурации которого 
    лежат в корне проекта в файле nginx-local.conf. 
    Для удобства используйте docker-compose-local.yaml, чтобы запустить локальный стэк.

    Переменные окружения конфигурируются в ./frontend/.env """

    dev: bool = Field(True)


class Settings(BaseSettings): 
    model_config = SettingsConfigDict(
        env_file=(
            ROOT_DIR / ".env",
            ROOT_DIR / 'frontend' / '.env',
        ),
        env_nested_delimiter='__',
        case_sensitive=False,
        extra='ignore' 
    )
    
    admin: AdminConfig = AdminConfig()
    db: DatabaseConfig = DatabaseConfig()
    auth_jwt: AuthJWT = AuthJWT() 
    logging: LoggingConfig = LoggingConfig()
    cookie: CookiesConfig = CookiesConfig() 
    redis: RedisConfig = RedisConfig() 
    rate_limit: RateLimitConfig = RateLimitConfig()
    docs: DocsConfig = DocsConfig()
    app: AppConfig = AppConfig()
    

settings = Settings() 
