import requests
from bs4 import BeautifulSoup


def garb_remove(string:str): 
    return ' '.join(string.split())


HEADERS = {
   "Accept": 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
   "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 YaBrowser/25.10.0.0 Safari/537.36'
}

url5413 = requests.get('https://rasp.rsreu.ru/schedule-frame/group?faculty=0&group=1633&date=').text
url5423 = requests.get('https://rasp.rsreu.ru/schedule-frame/group?faculty=4&group=1638&date=2025-11-03').text

LINKS = {
    '5413': url5413,
    '5423': url5423,
}

SCHEDULE_DATA = {}

#общее для всех (дни недели)
table_public = BeautifulSoup(LINKS['5413'], 'lxml').find('table')
if table_public: 
    dates = [garb_remove(date.text) for date in table_public.find_all('th')]

#индивидуально
for group, text in LINKS.items():
    soup = BeautifulSoup(text, 'lxml')

    table = soup.find('table') 
    lessons = [] #type-1 лек. type-2 лаба  type-3 упр
    if table: 
        span_list = [span.text.strip() for span in table.find_all('span')]
        for digit in '123':
            div_list = table.find_all('td', class_=f'schedule-cell schedule-lesson-type-{digit}')
            for td in div_list:
                td = garb_remove(td.text.strip())
                lessons.append(td)
        lessons = {group: lessons}
        SCHEDULE_DATA |= lessons


print(SCHEDULE_DATA)

print(dates)



