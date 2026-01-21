import logging
import time
from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from backend.api.core.config import Settings
from redis.asyncio import Redis


logger = logging.getLogger(__name__)


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, settings: Settings):
        super().__init__(app)
        self.settings = settings
    
    async def _atomic_incr_with_expire(
        self, 
        redis_client: Redis,
        key: str, 
        window_seconds: int
    ) -> int:
        """Атомарное увеличение счетчика с установкой TTL"""

        current_window_seconds = int(time.time()) // window_seconds
        window_key = f"{key}:{current_window_seconds}"
        
        # каждый window_key живет ровно window_seconds секунд
        current: int = await redis_client.incr(window_key)
        print(f'{current = }')
        # установим expire только если это первый incr для этого окна
        if current == 1:
            await redis_client.expire(window_key, window_seconds)
        
        return current
    
    async def dispatch(self, request: Request, call_next):
        ip = request.client.host
        window = self.settings.rate_limit.window_seconds
        redis_client: Redis | None = getattr(request.app.state, "redis", None)
        if redis_client is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Rate limiter unavailable")

        # проверка блокировки 
        if await redis_client.exists(f"block:{ip}"):
            logger.info("IP %s currently blocked for cooldown", ip)
            return JSONResponse(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                content={
                    "status": "429",
                    "detail": "превышен лимит запросов. подождите и попробуйте снова."
                },
            )
            

        # ключ на основе временного окна
        rate_key = f"rate:{ip}"

        # атомарное увеличение в текущем временном окне
        current = await self._atomic_incr_with_expire(redis_client, rate_key, window)
        
        if current > self.settings.rate_limit.max_requests:
            # блокировка если превышен лимит
            block_key = f"block:{ip}"
            await redis_client.set(
                block_key, 
                value=1, 
                ex=self.settings.rate_limit.cooldown_seconds
            )
            logger.warning("IP %s exceeded rate limit (%s reqs in %s sec) -> blocking for %s sec",
                           ip, current, window, self.settings.rate_limit.cooldown_seconds)
            return JSONResponse(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                content={
                    "status": "429",
                    "detail": "превышен лимит запросов."
                },
            )
            
        
        
        response = await call_next(request)
        logger.debug("[rate_limit] %s requests from %s in current window", current, ip)
        return response