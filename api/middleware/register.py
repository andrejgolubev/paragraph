from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.middleware.process_time import ProcessTimeHeaderMiddleware
from api.middleware.rate_limit import RateLimitMiddleware


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
        "https://192.168.0.108:8000",
    ]


def register_middlewares(app: FastAPI, settings):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOW_ORIGINS,
        allow_methods=["*"],  # Разрешить все методы (ПОКА ЧТО ДЛЯ РАЗРАБОТКИ)
        allow_headers=["*"],  # Разрешить все заголовки
        allow_credentials=True, # использую куки поэтому надо True 
        expose_headers=["*"],  # Позволяет фронтенду видеть Set-Cookie
    )

    app.add_middleware(ProcessTimeHeaderMiddleware)
    app.add_middleware(RateLimitMiddleware, settings=settings)
