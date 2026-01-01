from contextlib import asynccontextmanager
from fastapi import FastAPI
from .middleware import register_middlewares

def create_app() -> FastAPI:
    app = FastAPI(
        title='параграф'
        # lifespan=...
        # webhooks=...
    )

    # register_middlewares(app)
    return app




@asynccontextmanager
async def lifespan(app: FastAPI): 
    # redis = Redis( 
    #     ...
    # ) 
    ...

