
from fastapi import FastAPI
from contextlib import asynccontextmanager
from redis.asyncio import Redis

from .middleware.register import register_middlewares
from ..core.config import settings
from .logger import log


# def _build_redis_url() -> str:
#     host = settings.redis.host
#     port = settings.redis.port
#     db = settings.redis.db
#     password = settings.redis.password
#     if password:
#         return f"redis://:{password}@{host}:{port}/{db}"


@asynccontextmanager
async def lifespan(app: FastAPI):
    if not settings.app.dev: 
        redis_url = settings.redis.url  
    else: 
        redis_url = settings.redis.test_url

    redis_client = Redis.from_url(redis_url, decode_responses=True)

    await redis_client.ping()
    log.info('Redis startup')
    
    app.state.redis = redis_client
    yield

    await redis_client.aclose()
    log.info('Redis shutdown')


def create_app() -> FastAPI:
    app = FastAPI(
        title='параграф',
        lifespan=lifespan,
        # docs_url=None if not settings.docs.enabled else '/docs',
        # redoc_url=None if not settings.docs.enabled else '/redoc',
        docs_url='/docs',
        redoc_url='/redoc',
    )
    
    register_middlewares(app, settings)
    return app





