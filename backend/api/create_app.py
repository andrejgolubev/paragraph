
from fastapi import FastAPI
from contextlib import asynccontextmanager
from redis.asyncio import Redis

from .middleware.register import register_middlewares
from ..core.config import settings
from .logger import log



@asynccontextmanager
async def lifespan(app: FastAPI):
    redis_client = Redis.from_url(settings.redis.url, decode_responses=True)

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
        docs_url=None if not settings.docs.enabled else '/docs',
        redoc_url=None if not settings.docs.enabled else '/redoc',
    )
    
    register_middlewares(app, settings)
    return app





