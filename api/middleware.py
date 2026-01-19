import time
from fastapi import FastAPI, Response, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
# from api.auth.validation import get_access_token_payload
# from api.settings import settings

ALLOW_ORIGINS = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "http://192.168.0.108:5173",
        "http://192.168.0.108:8000",
        "http://192.168.0.102:8000",
        # для https 
        "https://localhost:5173",
        "https://127.0.0.1:5173",
        "https://localhost:8000",
        "https://127.0.0.1:8000",
        "https://192.168.0.108:5173",
        "https://192.168.0.108:5174",
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


def register_middlewares(app: FastAPI):

    app.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOW_ORIGINS,
        allow_methods=["*"],  # Разрешить все методы (ПОКА ЧТО ДЛЯ РАЗРАБОТКИ)
        allow_headers=["*"],  # Разрешить все заголовки
        allow_credentials=True, # использую куки поэтому надо True 
        expose_headers=["*"],  # Позволяет фронтенду видеть Set-Cookie
    )

    app.add_middleware(ProcessTimeHeaderMiddleware)
