from ..api.routers import schedule, homework, database
from ..api.auth.users import router as user_router
from .auth.admin import router as admin_router
from .create_app import create_app
from .logger import log



app = create_app()

for router in (
    user_router,
    admin_router,
    schedule.schedule_router,
    homework.homework_router,
    database.database_router,
):  
    app.include_router(router)
     

