import time
from fastapi import FastAPI, Response, Request
from fastapi.middleware.cors import CORSMiddleware
import jwt
from sqlalchemy import select
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from api.auth.users import get_refreshed_access_token
from api.auth.utils import encode_jwt
from api.auth.validation import get_refresh_token_payload
from api.db.database import AsyncSessionLocal
from api.db.models import User
from api.settings import settings
from api.auth import utils as auth_utils

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
        response = await call_next(request)
        excluded_paths = ['/favicon.ico', '/openapi.json', '/redoc', '/static/', '/user/login']
        if any(request.url.path.startswith(path) for path in excluded_paths):
            return response

        async with AsyncSessionLocal() as session: 
            access_token = await get_refreshed_access_token(payload=payload, db=session)


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
        allow_headers=["*"],  # Разрешить все заголовки
        allow_credentials=True # использую куки
    )

    app.add_middleware(RefreshToken)

    app.add_middleware(ProcessTimeHeaderMiddleware)
