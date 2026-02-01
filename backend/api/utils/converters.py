from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.db.models import Group


def convert_date(date: str): 
    """date подаётся в формате в таком, в котором юзер ее выбирает из списка на фронтенде для последующей конвертации 
    в пригодную для вставки в ссылку и парсинга сайта ргрту. т.е. (10.11.2025, числ.) -> 2025-11-10  """
    return '-'.join(reversed(date[:10].split('.'))) 


async def get_group_datavalue_by_group_number(
    group_number: str,
    db: AsyncSession,
):
    """конвертирует group_datavalue в group_number"""
    group = (await db.scalars(
        select(Group).where(Group.group_number == group_number)
    )).first()
    
    return group.data_value


def latin_to_cyrillic(input_str: str) -> str:
    """
    заменяет латинские буквы, похожие на кириллические, на соответствующие кириллические.
    """
    if not input_str or not isinstance(input_str, str):
        return input_str
    
    latin_to_cyrillic_map = {
        'A': 'А', 'B': 'В', 'C': 'С', 'E': 'Е', 'K': 'К',
        'M': 'М', 'H': 'Н', 'O': 'О', 'P': 'Р', 'T': 'Т',
        'X': 'Х', 'Y': 'У'
    }
    
    # заменяем символы
    result = ''.join(
        latin_to_cyrillic_map.get(char, char)
        for char in input_str
    )
    
    return result 







