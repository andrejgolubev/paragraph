"""File with settings and configs for the project"""
from envparse import Env
from dotenv import load_dotenv
import os

env = Env()

REAL_DATABASE_URL = env.str(
    "REAL_DATABASE_URL",
    default="postgresql+asyncpg://pg:root@127.0.0.1:5433/pg"
)  # connect string for the database


load_dotenv() 
if os.getenv('SECRET_KEY'): SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = "HS256"


