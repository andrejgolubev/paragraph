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


    
    final_group = group_data_value or request.cookies.get("selected_group")
    final_date = date_data_value or request.cookies.get("selected_date")
    
    if not final_group:
        return {"error": "Group not selected"}

    # Формируем URL
    url = f'https://rasp.rsreu.ru/schedule-frame/group?faculty=1&group={final_group}&date={final_date or ""}'    

    try:
        # Парсим расписание
        schedule_data = await parse_schedule_from_url(url)
        print("SCHEDULE DATA STRUCTURE:", schedule_data)  
        # return {
        #     "group_data_value": final_group,
        #     "date_data_value": final_date,
        #     "schedule_data": schedule_data
        # }
        return schedule_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error parsing schedule: {str(e)}")


from api.db.schemas import GroupSelection

@router.post("/select-group")
async def select_group(
    group_data: GroupSelection,
    response: Response,
    db: AsyncSession = Depends(get_db)
):
    # Сохраняем в cookie на 30 дней
    response.set_cookie(
        key="selected_group",
        value=group_data.group_data_value,
        max_age=30*24*60*60,  # 30 дней
        httponly=True,
        secure=True  # для HTTPS
    )
    
    return {"status": "success", "selected_group": group_data.group_data_value} 

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