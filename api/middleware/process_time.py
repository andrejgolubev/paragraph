import time
from fastapi import Response, Request
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

class ProcessTimeHeaderMiddleware(BaseHTTPMiddleware): 
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        start = time.perf_counter()
        response = await call_next(request) # вызов эндпоинта 
        process_time = time.perf_counter() - start
        response.headers["X-Process-Time"] = f'{process_time:.5f}' 

        return response