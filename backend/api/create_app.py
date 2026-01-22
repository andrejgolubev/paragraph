import logging
from fastapi import FastAPI
from contextlib import asynccontextmanager
from redis.asyncio import Redis
from backend.api.middleware.register import register_middlewares
from backend.core.config import settings

log = logging.getLogger(__name__)

def _build_redis_url() -> str:
    host = settings.redis.host
    port = settings.redis.port
    db = settings.redis.db
    password = settings.redis.password
    if password:
        return f"redis://:{password}@{host}:{port}/{db}"
    return f"redis://{host}:{port}/{db}"



@asynccontextmanager
async def lifespan(app: FastAPI):
    redis_url = _build_redis_url()
    redis_client = Redis.from_url(redis_url, decode_responses=True)

    await redis_client.ping()
    log.info('Redis работает')
    
    app.state.redis = redis_client
    yield

    await redis_client.close()
    log.info('Redis отключен')


def create_app() -> FastAPI:
    app = FastAPI(
        title='параграф',
        lifespan=lifespan,
        # webhooks=...
    )
    
    register_middlewares(app, settings)
    return app





