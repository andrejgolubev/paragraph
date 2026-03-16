from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .log import LogMiddleware
from ..middleware.rate_limit import RateLimitMiddleware


ALLOW_ORIGINS = [
    "http://localhost:5173",
    "http://localhost:8000",
    # для https локально
    "https://192.168.0.104:5173",
    "https://192.168.0.104:8000",
    "https://paragraph-schedule.ru",
    "https://www.paragraph-schedule.ru",
    "https://api.paragraph-schedule.ru",
    "https://www.api.paragraph-schedule.ru",
]



def register_middlewares(app: FastAPI, settings):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOW_ORIGINS,
        allow_methods=["*"],
        allow_headers=["*"],
        allow_credentials=True,
    )

    app.add_middleware(RateLimitMiddleware, settings=settings)
    app.add_middleware(LogMiddleware)
