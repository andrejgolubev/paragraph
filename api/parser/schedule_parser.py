import requests
from bs4 import BeautifulSoup
import asyncio

def garb_remove(string: str): 
    return ' '.join(string.split())


def parse_schedule(url: str) -> dict[str, list]: 
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    table = soup.find('table')
    
    if not table:
        return {"error": "Table not found"}
    
    result = {
        "days": [],  # заголовки дней
        "schedule": []  # расписание по времени
    }
    
    # header_row - строка, где лежат даты и названия дней недели
    header_row = table.find('tr', class_='table-row-height-large')
    if header_row:
        day_headers = header_row.find_all('th')[1:]  # пропускаем первый th "Время"
        for th in day_headers:
            span = th.find('span')
            date_text = span.get_text(strip=True) if span else ""
            day_text = th.get_text().replace(date_text, '').strip()
            result["days"].append({
                "date": date_text,
                "day": day_text
            })
    
    # парсим время
    time_rows = table.find_all('tr')[1:]  # пропускаем заголовок
    
    for row in time_rows:
        # пропускаем пустые строки
        if not row.find('td'):
            continue
        
        time_cell = row.find('td')
        if time_cell:
            time_divs = time_cell.find_all('div')
            time_start = time_divs[0].get_text(strip=True) 
            time_end = time_divs[1].get_text(strip=True) 
        
        time_slot = {
            "time_start": time_start,
            "time_end": time_end,
            "lessons": []
        }
        
         # берем 6 ячеек с занятиями (пн-сб)
        lesson_cells = row.find_all('td')[1:7] 
        
        for cell in lesson_cells: 
            lessons_in_cell = []
            
            lesson_divs = cell.find_all('div', recursive=False)


            for div in lesson_divs:
                lesson_data = {}
                
                type_badge = div.find('span') # тип занятия (Лек., Лаб., Упр.)
                if type_badge:
                    lesson_data["type"] = garb_remove(type_badge.get_text(strip=True))
                

                lesson_text = div.get_text()
                if type_badge: # после строки ниже в lesson_text будет лежать всё кроме type_badge
                    lesson_text = lesson_text.replace(type_badge.get_text(), '').strip()

                #очищаем от пробелов                
                lesson_data["text"] = ', '.join(garb_remove(lesson_text).split(','))
                
                if lesson_data:  # добавляем только если есть данные
                    lessons_in_cell.append(lesson_data)


            time_slot["lessons"].append(lessons_in_cell)
        
        result["schedule"].append(time_slot)
    
    return result



async def parse_schedule_from_url(url: str, function=parse_schedule):
    """Для синхронных парсеров используем thread pool"""
    # вся эта инструкция нужна тк parse_schedule - синхронный парсер
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, function, url)  


