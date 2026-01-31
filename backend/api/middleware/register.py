from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .log import LogMiddleware
from ..middleware.rate_limit import RateLimitMiddleware


ALLOW_ORIGINS = [
        "http://localhost:5173",
        "http://localhost:8000",
        "http://192.168.0.108:5173",
        "http://192.168.0.108:8000",
        # для https локально
        "https://localhost:5173",
        "https://localhost:8000",
        "https://192.168.0.108:5173",
        "https://192.168.0.108:8000",

        "https://paragraph-schedule.ru",
        "https://www.paragraph-schedule.ru",
        "https://api.paragraph-schedule.ru",
        "https://www.api.paragraph-schedule.ru",
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

    app.add_middleware(RateLimitMiddleware, settings=settings)
    app.add_middleware(LogMiddleware)