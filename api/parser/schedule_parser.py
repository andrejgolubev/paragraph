import requests
from bs4 import BeautifulSoup
from group_parser import parse_groups

def garb_remove(string: str): 
    return ' '.join(string.split())


def get_datavalue_by_number(number: str): 
    return parse_groups()[number]


def get_number_by_data_value(data_value): 
    return {key:value for value, key in parse_groups().items()}[data_value]


def parse_by_url(url: str): 
    try:
        response = requests.get(url)
    except Exception:
        raise Exception('Не валидный URL') 
    _gr_find = url.find('group=') + 6
    data_value = ''.join([ch for ch in url[_gr_find: _gr_find + 6] if ch.isdigit()])
    group_number = get_number_by_data_value(data_value)
    _dt_find = url.find('date=') + 5 
    date = url[_dt_find:]
    soup = BeautifulSoup(response.text, 'lxml')
    table = soup.find('table') 

    lessons = [] 
    if table: 
        div_list = table.find_all('td')
        for td in div_list:
            td = garb_remove(td.text.strip())
            if ':' not in td:
                lessons.append(td)

        lessons = [(group_number, date), lessons]
    return lessons

def convert_date(date: str): 
    """date подаётся в формате в таком, в котором юзер ее выбирает из списка на фронтенде для последующей конвертации 
    в пригодную для вставки в ссылку и парсинга сайта ргрту. т.е. (10.11.2025, числ.) -> 2025-11-10  """
    return '-'.join(reversed(date[:10].split('.')))

if __name__ == '__main__':
    parsed = parse_by_url('https://rasp.rsreu.ru/schedule-frame/group?faculty=4&group=878&date=2025-11-10')
    converted = parsed[0][1] 
    print(parsed, converted)

# with open('schedule.json', 'w') as file:
#     json.dump(SCHEDULE_DATA, file)


# with open('schedule.json', 'r') as file:
#     a = json.load(file)
#     print(a)