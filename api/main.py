import asyncio
from fastapi import FastAPI, Depends, Request
from api.routers.users import user_router
from api.auth import oauth2_scheme
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from api.parser.OLD_parser import SCHEDULE_DATA
from sqlalchemy.ext.asyncio import AsyncSession
from db.database import get_db
import time
from api.parser.group_parser import parse_all_groups
from db.schemes import GroupCreate
from db.models import Group
from sqlalchemy import select


async def lifespan(app: FastAPI):
    # Startup
    print("🚀 Starting application...")
    
    # Запускаем синхронизацию в фоне
    asyncio.create_task(sync_db_data_on_startup())
    
    yield
    # Shutdown
    print("👋 Shutting down application...")

app = FastAPI(title="PROGINZH", lifespan=)

GROUPS_DICT = parse_all_groups()
print(GROUPS_DICT)


async def sync_db_data_on_startup():
    """Синхронизация данных при запуске приложения"""
    await asyncio.sleep(5)  # Ждем немного чтобы приложение полностью запустилось
    print("🔄 Starting database synchronization...")
    
    try:
        # Используем dependency для получения сессии
        async for db in get_db():
            # Парсим группы (синхронно в отдельном потоке)
            loop = asyncio.get_event_loop()
            groups_dict = await loop.run_in_executor(
                None, 
                parser_service.parse_all_groups
            )
            
            if groups_dict:
                await save_groups_to_db(db, groups_dict)
            break
            
    except Exception as e:
        print(f"❌ Error during startup sync: {e}")

async def save_groups_to_db(db: AsyncSession = Depends(get_db)): 
    skipped = added = 0
    try:
        for group_number, data in GROUPS_DICT.items(): 
            result = await db.execute(
                    select(Group).where(Group.data_value == data))
            
            existing_group = result.scalar_one_or_none()
            if not existing_group:
                group = GroupCreate(group_number=group_number, data_value=data)
                db.add(group) 
                added += 1
            else: skipped += 1

            await db.commit()
            print(f"Saved {added} groups to database, skipped {skipped} groups.")
                # await db.refresh(gr)
    except Exception as e:
        await db.rollback()
        print(f"❌ Error saving groups: {e}")

async def main():
    await sync_db_data()
    await asyncio.sleep(30)  # Асинхронная задержка


# монтируем CSS, js, png etc
# app.mount("/static", StaticFiles(directory="./static"), name="static")
templates = Jinja2Templates(directory="templates")
# create the instance for the routes

app.include_router(
    user_router,
    prefix="/user",
    tags=["users"],
    dependencies=[Depends(oauth2_scheme)],
)




@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse(
        name="index.html", request=request, context={
            "SCHEDULE": SCHEDULE_DATA,
        }
    )






