import time
from fastapi import FastAPI, Response, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from api.auth.users import get_refreshed_access_token
from api.auth.validation import get_refresh_token_payload
from api.db.database import AsyncSessionLocal
from api.settings import settings

ALLOW_ORIGINS = [
    "http://localhost:8000",
    "http://localhost:5173", # frontend
]

class ProcessTimeHeaderMiddleware(BaseHTTPMiddleware): 
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        start = time.perf_counter()
        response = await call_next(request) # вызов эндпоинта 
        process_time = time.perf_counter() - start
        response.headers["X-Process-Time"] = f'{process_time:.5f}' 

        return response


class RefreshToken(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        payload = get_refresh_token_payload(request=request)
        async with AsyncSessionLocal() as session: 
            access_token = await get_refreshed_access_token(payload=payload, db=session)

            response = await call_next(request)
            response.set_cookie(
                key='access_token',
                value=access_token,
                httponly=True,
                secure=True,  # только для htpps
                samesite="strict",  # защита от csrf
                max_age=settings.auth_jwt.access_token_expire_minutes*60
            )

        return response


def register_middlewares(app: FastAPI):

    app.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOW_ORIGINS,
        allow_methods=["*"],  # Разрешить все методы (ПОКА ЧТО ДЛЯ РАЗРАБОТКИ)
        allow_headers=["*"],  # Разрешить все заголов
    )

    app.add_middleware(
        ProcessTimeHeaderMiddleware,
    )

    app.add_middleware(RefreshToken)
    ...


