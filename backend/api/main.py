import logging
from fastapi import FastAPI
from backend.api.routers import schedule, homework, database
from backend.api.auth.users import router as user_router
from backend.api.auth.admin import router as admin_router
from backend.api.create_app import create_app
from backend.core.config import settings

logging.basicConfig(
    level=settings.logging.log_level_value,
    format=settings.logging.log_format,
)

log = logging.getLogger(__name__)


app: FastAPI = create_app()

for router in (
    user_router,
    admin_router,
    schedule.schedule_router,
    homework.homework_router,
    database.database_router,
):  
    app.include_router(router)
     

