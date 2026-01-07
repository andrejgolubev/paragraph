import time
from fastapi import FastAPI, HTTPException, Response, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from api.auth.users import get_refreshed_access_token
from api.auth.validation import get_refresh_token_payload
from api.db.database import AsyncSessionLocal
from api.settings import settings

ALLOW_ORIGINS = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "http://192.168.0.108:5173",
        "http://192.168.0.108:8000",
        "http://192.168.0.102:8000",
        # вот эти все для https надо?
        "https://localhost:5173",
        "https://127.0.0.1:5173",
        "https://localhost:8000",
        "https://127.0.0.1:8000",
        "https://192.168.0.108:5173",
        "https://192.168.0.108:8000",
        "https://192.168.0.102:8000",
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

        if request.method == "OPTIONS":
            return await call_next(request)

        excluded_paths = ['/favicon.ico', '/openapi.json', '/redoc', '/static/', '/user/login', '/user/logout', '/homework/get']
        if any(request.url.path.startswith(path) for path in excluded_paths):
            return await call_next(request)

        try:
            payload = get_refresh_token_payload(request=request)
            
            async with AsyncSessionLocal() as session: 
                access_token = await get_refreshed_access_token(payload=payload, db=session)
            
            response = await call_next(request)
            
            response.set_cookie(
                key='access_token',
                value=access_token,
                httponly=True,
                secure=True,  # но можно False для localhost
                samesite='none', # обязательно 'lax' для продакшна 
                max_age=settings.auth_jwt.access_token_expire_minutes * 60
            )
            
            return response
            
        except HTTPException:
            # ели нет валидного refresh token, просто пропускаем обновление
            # НЕ выбрасываем исключение, а продолжаем цепочку
            return await call_next(request)
        except Exception:
            # любая другая ошибка - тоже пропускаем
            return await call_next(request)


def register_middlewares(app: FastAPI):

    app.add_middleware(
        CORSMiddleware,
        # allow_origins=['*'],
        allow_origins=ALLOW_ORIGINS,
        allow_methods=["*"],  # Разрешить все методы (ПОКА ЧТО ДЛЯ РАЗРАБОТКИ)
        allow_headers=["*"],  # Разрешить все заголовки
        allow_credentials=True, # использую куки поэтому надо True 
        expose_headers=["*"],  # Позволяет фронтенду видеть Set-Cookie
    )

    app.add_middleware(RefreshToken)

    app.add_middleware(ProcessTimeHeaderMiddleware)
