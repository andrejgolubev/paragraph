import logging
import uvicorn
from api.settings import settings

from api.db.refresh_db import load_groups_and_dates

from api.db.database import get_db
from api.routers import schedule, homework, database
from api.auth.users import router as user_router
from api.parser.group_parser import parse_groups
from api.parser.date_parser import parse_dates
from api.parser.utils import convert_date
from api.auth.utils import verify_admin_api_key
from api.db.models import Group, Date

from fastapi import Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from api.create_app import create_app


# logging.basicConfig(
#     level=settings.logging.log_level_value,
#     format=settings.logging.log_format,
# )

# log = logging.getLogger(__name__)


app = create_app()

app.include_router(user_router)
app.include_router(schedule.schedule_router)
app.include_router(homework.homework_router)
app.include_router(database.database_router)
     

if __name__ == "__main__":
    uvicorn.run(
        app,
        port=8000,
        log_level="info",
        # reload=True
    )
