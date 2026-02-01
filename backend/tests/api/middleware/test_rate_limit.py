import time

import pytest
from fastapi import FastAPI
from httpx import AsyncClient, ASGITransport
from types import SimpleNamespace
from asgi_lifespan import LifespanManager

from redis.asyncio import Redis

from backend.api.middleware.rate_limit import RateLimitMiddleware
from backend.core.config import settings
from backend.api.main import app as main_app

class _TestRateLimitSettings:
    def __init__(self) -> None:
        self.rate_limit = SimpleNamespace(
            max_requests=1,
            window_seconds=60,
            cooldown_seconds=5,
        )


TEST_RATE_LIMIT_SETTINGS = _TestRateLimitSettings()


# @pytest.fixture
# async def redis_client() -> Redis:
#     async with LifespanManager(main_app):
#         client: Redis = main_app.state.redis
        

#     keys = await client.keys("rate:*")
#     if keys:
#         await client.delete(*keys)
#     await client.delete("block:127.0.0.1")

#     return client

@pytest.fixture
async def local_app(redis_client: Redis) -> FastAPI:
    app = FastAPI()
    app.state.redis = redis_client
    app.add_middleware(RateLimitMiddleware, settings=TEST_RATE_LIMIT_SETTINGS)

    @app.get("/health")
    async def health_check():
        return {"status": "ok"}

    return app


def _build_rate_key() -> str:
    window = int(time.time()) // TEST_RATE_LIMIT_SETTINGS.rate_limit.window_seconds
    return f"rate:127.0.0.1:{window}"


@pytest.mark.asyncio(loop_scope="session")
async def test_rate_limit_blocks_after_second_request(
    local_app: FastAPI,
    redis_client: Redis,
) -> None:
    """Проверяем, что middleware блокирует слишком частые запросы."""
    rate_key = _build_rate_key()
    block_key = "block:127.0.0.1"
    await redis_client.delete(rate_key, block_key)

    async with AsyncClient(
        transport=ASGITransport(local_app),
        base_url="http://127.0.0.1",
    ) as client:
        first = await client.get("/health")
        second = await client.get("/health")

    assert first.status_code == 200
    assert second.status_code == 429

    assert await redis_client.exists(block_key) == 1
    total_requests = await redis_client.get(rate_key)
    assert total_requests is not None
    assert int(total_requests) >= 2

