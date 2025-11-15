from fastapi import Request, HTTPException, APIRouter, Depends
from api.db.database import get_db
from api.parser.schedule_parser import parse_schedule_from_url  # твой существующий парсер
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
schedule_router = APIRouter(tags=['Schedule'], prefix='/schedule')

router = schedule_router

@router.get("/get-schedule")
async def get_schedule(
    request: Request,
    group_data_value: str | None = None,
    date_data_value: str | None = None,
    db: AsyncSession = Depends(get_db)
):
    # Если параметры не переданы, пытаемся взять из cookie
    if not group_data_value:
        group_data_value = request.cookies.get("selected_group")
    if not date_data_value:
        date_data_value = request.cookies.get("selected_date")
    
    if not group_data_value:
        raise HTTPException(status_code=400, detail="Group not selected")
    
    # Формируем URL
    url = f'https://rasp.rsreu.ru/schedule-frame/group?faculty=1&group={group_data_value}&date={date_data_value or ""}'
    
    try:
        # Парсим расписание
        schedule_data = await parse_schedule_from_url(url)
        return schedule_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error parsing schedule: {str(e)}")
