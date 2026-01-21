import os
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi import FastAPI
from backend.api.middleware.register import register_middlewares
from redis.asyncio import Redis
from backend.api.core.config import settings


load_dotenv()


def _build_redis_url() -> str:
    host = os.getenv("REDIS_HOST")
    port = os.getenv("REDIS_PORT", "6380")
    db = os.getenv("REDIS_DB", "0")
    password = os.getenv("REDIS_PASSWORD")
    if password:
        return f"redis://:{password}@{host}:{port}/{db}"
    return f"redis://{host}:{port}/{db}"



@asynccontextmanager
async def lifespan(app: FastAPI):
    redis_url = _build_redis_url()
    redis_client = Redis.from_url(redis_url, decode_responses=True)

    await redis_client.ping()
    print("Redis работает")
    app.state.redis = redis_client
    yield
    await redis_client.close()
    print("Redis отключен")


def create_app() -> FastAPI:
    app = FastAPI(
        title='параграф',
        lifespan=lifespan,
        # webhooks=...
    )

    
    register_middlewares(app, settings)
    return app





