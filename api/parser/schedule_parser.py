import requests
from bs4 import BeautifulSoup
from api.parser.group_parser import parse_groups
import asyncio
import re 
from functools import lru_cache
import hashlib
from datetime import datetime, timedelta

def garb_remove(string: str): 
    return ' '.join(string.split())


def get_datavalue_by_number(number: str): 
    return parse_groups()[number]


def get_number_by_data_value(data_value): 
    return {key:value for value, key in parse_groups().items()}[data_value]


#старый парсер
def parse_schedule(url: str): 
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



class FastScheduleParser:
    """парсер с кэшированием"""
    
    # Предкомпилированные regex для скорости
    WHITESPACE_REGEX = re.compile(r'\s+')
    BRACKETS_REGEX = re.compile(r'\s*\(.*?\)')
    
    def __init__(self, cache_ttl_minutes: int = 30):
        self.cache = {}
        self.cache_ttl = timedelta(minutes=cache_ttl_minutes)
    
    def _clean_text(self, text: str) -> str:
        """Быстрая очистка текста"""
        if not text:
            return ""
        text = self.WHITESPACE_REGEX.sub(' ', text.strip())
        return text
    
    def _extract_lesson_type(self, badge) -> str:
        """Извлечение типа занятия из badge"""
        if not badge:
            return ""
        
        text = badge.get_text(strip=True)
        # Убираем иконки (текст внутри i тегов)
        for icon in badge.find_all('i'):
            icon_text = icon.get_text()
            text = text.replace(icon_text, '').strip()
        
        return self._clean_text(text)
    
    def _parse_lesson(self, div) -> dict:
        """Быстрый парсинг одного занятия"""
        badge = div.find('span', class_='schedule-lesson-type-badge')
        lesson_type = self._extract_lesson_type(badge)
        
        text = div.get_text()
        if badge:
            badge_text = badge.get_text()
            text = text.replace(badge_text, '', 1)
        
        text = self._clean_text(text)
        
        result = {"text": ', '.join(text.split(','))}
        if lesson_type:
            result["type"] = lesson_type
        
        return result
    
    def _parse_row(self, row) -> dict | None:
        """Парсинг одной строки таблицы"""
        cells = row.find_all('td')
        if len(cells) < 7:
            return None
        
        # Время
        time_divs = cells[0].find_all('div')
        time_data = {
            "time_start": self._clean_text(time_divs[0].get_text()) if time_divs else "",
            "time_end": self._clean_text(time_divs[1].get_text()) if len(time_divs) > 1 else "",
            "lessons": []
        }
        
        for i in range(1, 7):
            cell = cells[i]
            day_lessons = []
            
            # Основные занятия
            for div in cell.find_all('div', recursive=False):
                if 'schedule-cell-subgroup-item' not in div.get('class', []):
                    lesson = self._parse_lesson(div)
                    if lesson and lesson['text']:
                        day_lessons.append(lesson)
            
            # Подгруппы
            for div in cell.find_all('div', class_='schedule-cell-subgroup-item'):
                lesson = self._parse_lesson(div)
                
                if lesson and lesson['text']:
                    day_lessons.append(lesson)
            
            time_data["lessons"].append(day_lessons)
            
        
        return time_data
    
    @lru_cache(maxsize=100)
    def parse(self, url: str, use_cache: bool = True) -> dict:
        """Основной метод парсинга с кэшированием"""
        cache_key = hashlib.md5(url.encode()).hexdigest()
        
        if use_cache:
            cached = self.cache.get(cache_key)
            if cached and datetime.now() - cached['time'] < self.cache_ttl:
                return cached['data']
        
        # Загрузка
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'lxml')
        
        # Поиск таблицы
        table = soup.find('table', class_='table-vertical-borders')
        if not table:
            result = {"error": "Table not found"}
        else:
            # Заголовок с днями
            days = []
            header = table.find('tr', class_='table-row-height-large')
            if header:
                for th in header.find_all('th')[1:]:
                    span = th.find('span')
                    date = self._clean_text(span.get_text()) if span else ""
                    day_text = self._clean_text(th.get_text()).replace(date, '').strip()
                    day_text = self.BRACKETS_REGEX.sub('', day_text)

                    days.append({"date": date, "day": day_text})
            
            schedule = []
            for row in table.find_all('tr')[1:]:
                time_slot = self._parse_row(row)
                if time_slot:
                    schedule.append(time_slot)
            
            result = {"days": days, "schedule": schedule}
        
        # Кэширование
        if use_cache:
            self.cache[cache_key] = {
                'data': result,
                'time': datetime.now()
            }
        
        return result




async def parse_schedule_from_url(url: str, function=parse_schedule):
    """Для синхронных парсеров используем thread pool"""
    # вся эта инструкция нужна тк parse_schedule - синхронный парсер
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, function, url)  


if __name__ == '__main__':
    parsed = parse_schedule('https://rasp.rsreu.ru/schedule-frame/group?faculty=4&group=878&date=2025-11-10')
