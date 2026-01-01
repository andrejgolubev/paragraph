from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware


ALLOW_ORIGINS = [
    "http://localhost:8000",
    "http://localhost:5173", # frontend
]



def register_middlewares(app: FastAPI):

    app.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOW_ORIGINS,
        allow_methods=["*"],  # Разрешить все методы (ПОКА ЧТО ДЛЯ РАЗРАБОТКИ)
        allow_headers=["*"],  # Разрешить все заголов
    )


# class CustomCORSMiddleware(BaseHTTPMiddleware):

#     async def dispatch(self, request: Request, call_next):
#         '''основной метод middleware, который вызывается для каждого запроса'''
#         origin = request.headers.get("origin")
#         print(f'{request = }')
#         print(f'{request.headers = }')
#         print(f'{origin = }')

#         # проверяем origin и устанавливаем заголовки
#         response = await call_next(request)
        
#         if origin and request.method == "GET":
#             response.headers["Access-Control-Allow-Origin"] = "*"
#             response.headers["Access-Control-Allow-Methods"] = "GET"
#             response.headers["Access-Control-Allow-Headers"] = "*"

#         elif origin in ["http://localhost:8000", "http://localhost:5173"]:
#             response.headers["Access-Control-Allow-Origin"] = origin
#             response.headers["Access-Control-Allow-Methods"] = "*"
#             response.headers["Access-Control-Allow-Headers"] = "*"
#             response.headers["Access-Control-Allow-Credentials"] = "true"
        
#         return response