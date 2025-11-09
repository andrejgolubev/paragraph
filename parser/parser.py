import requests
from bs4 import BeautifulSoup

def garb_remove(string: str): 
    return ' '.join(string.split())


HEADERS = {
   "Accept": 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
   "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 YaBrowser/25.10.0.0 Safari/537.36'
}

url543z = requests.get('https://rasp.rsreu.ru/schedule-frame/group?faculty=4&group=1639&date=2025-11-03').text
url543c = requests.get('https://rasp.rsreu.ru/schedule-frame/group?faculty=4&group=1639&date=2025-11-10').text
url5413z = requests.get('https://rasp.rsreu.ru/schedule-frame/group?faculty=0&group=1633&date=').text
url5413с = requests.get('https://rasp.rsreu.ru/schedule-frame/group?faculty=4&group=1633&date=2025-11-10').text
url5423z = requests.get('https://rasp.rsreu.ru/schedule-frame/group?faculty=4&group=1638&date=2025-11-03').text
url5423c = requests.get('https://rasp.rsreu.ru/schedule-frame/group?faculty=4&group=1638&date=2025-11-10').text

LINKS = {
    '543z':url543z,
    '543c': url543c,
    '5413z': url5413z,
    '5423c': url5423z,
    '5423z': url5423z,
    '5423c': url5423c,
}

SCHEDULE_DATA = {}

#общее для всех (дни недели)
table_public = BeautifulSoup(LINKS['5413z'], 'lxml').find('table')
if table_public: WEEK_DAYS = [garb_remove(date.text) for date in table_public.find_all('th')][1:]

#индивидуально
for group, text in LINKS.items():
    soup = BeautifulSoup(text, 'lxml')

    table = soup.find('table') 
    lessons = [] #type-1 лек. type-2 лаба  type-3 упр
    if table: 
        span_list = [span.text.strip() for span in table.find_all('span')]
        # div_list = table.find_all('td', class_='schedule-cell schedule-cell-non-working-day')
        div_list = table.find_all('td')
        for td in div_list:
            td = garb_remove(td.text.strip())
            if ':' not in td:
                lessons.append(td)
        lessons = {group: lessons}
        SCHEDULE_DATA |= lessons

print(WEEK_DAYS)









# with open('schedule.json', 'w') as file:
#     json.dump(SCHEDULE_DATA, file)


# with open('schedule.json', 'r') as file:
#     a = json.load(file)
#     print(a)