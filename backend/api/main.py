from ..api.routers import schedule, database
from ..api.auth.users import router as user_router
from ..api.tasks.homework import router as homework_router
from ..api.tasks.notes import router as notes_router
from .auth.admin import router as admin_router
from .create_app import create_app
from .logger import log



app = create_app()

for router in (
    user_router,
    admin_router,
    schedule.schedule_router,
    homework_router,
    notes_router,
    database.database_router,
):  
    app.include_router(router)
     

