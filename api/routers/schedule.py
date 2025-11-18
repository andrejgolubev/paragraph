from fastapi import Request, Response, HTTPException, APIRouter, Depends
from fastapi.responses import JSONResponse
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

from datetime import datetime, timedelta


@router.post("/select-group")
async def select_group(
    group_data_value: str,
    response: Response,
    db: AsyncSession = Depends(get_db)
):
    # Сохраняем в cookie на 30 дней
    response.set_cookie(
        key="selected_group",
        value=group_data_value,
        max_age=30*24*60*60,  # 30 дней
        httponly=True,
        secure=True  # для HTTPS
    )
    
    # Можно также сохранить в БД если нужно
    return {"status": "success", "message": "Group selected"} 

from api.services.data_service import data_service

@router.get('/get-all-groups', response_class=JSONResponse)
async def get_all_groups(db: AsyncSession = Depends(get_db)): 
    return await data_service.get_all_groups(db)


@router.get('/get-all-dates', response_class=JSONResponse)
async def get_all_dates(db: AsyncSession = Depends(get_db)): 
    dates = await data_service.get_all_dates(db) 
    return [
        {
            "date": date.date,
            'data_value': date.data_value,
        }
        for date in dates
    ]