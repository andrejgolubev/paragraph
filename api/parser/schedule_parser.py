import requests
from bs4 import BeautifulSoup
from api.parser.group_parser import parse_groups
import asyncio

def garb_remove(string: str): 
    return ' '.join(string.split())


def get_datavalue_by_number(number: str): 
    return parse_groups()[number]


def get_number_by_data_value(data_value): 
    return {key:value for value, key in parse_groups().items()}[data_value]



def parse_schedule(url: str): 
    response = requests.get(url)
    # _gr_find = url.find('group=') + 6
    # data_value = ''.join([ch for ch in url[_gr_find: _gr_find + 6] if ch.isdigit()])
    # group_number = get_number_by_data_value(data_value)
    # _dt_find = url.find('date=') + 5 
    # date = url[_dt_find:]
    soup = BeautifulSoup(response.text, 'lxml')
    table = soup.find('table') 

    lessons = [] 
    if table: 
        div_list = table.find_all('td')
        for td in div_list:
            td = garb_remove(td.text.strip())
            if ':' not in td:
                lessons.append(td)

        # lessons = [(group_number, date), lessons]
    return lessons



async def parse_schedule_from_url(url: str):
    """Для синхронных парсеров используем thread pool"""
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, parse_schedule, url)  # parse_schedule - твой синхронный парсер



if __name__ == '__main__':
    parsed = parse_schedule('https://rasp.rsreu.ru/schedule-frame/group?faculty=4&group=878&date=2025-11-10')
    converted = parsed[0][1] 
    print(parsed, converted)
