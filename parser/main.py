import requests
from bs4 import BeautifulSoup

def garb_remove(string:str): 
    return ' '.join(string.split())

# st_accept = "text/html" # говорим веб-серверу, 
#                         # что хотим получить html
# # имитируем подключение через браузер Mozilla на macOS

# st_useragent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_3_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15"
# # формируем хеш заголовков
# headers = {
#    "Accept": st_accept,
#    "User-Agent": st_useragent
# }

text = requests.get('https://rasp.rsreu.ru/schedule-frame/group?faculty=0&group=1633&date=').text
soup = BeautifulSoup(text, 'lxml')

table = soup.find('table') 
lessons = [] #type-1 лек. type-2 лаба  type-3 упр
if table: 
    span_list = [span.text.strip() for span in table.find_all('span')]
    # lessons = [les for les in span_list if '.' in les] # НЕ УДАЛЯТЬ, ПОКА НЕ НУЖЕН
    # dates = [date for date in span_list if any(s.isdigit() for s in date)]
    for digit in '123':
        div_list = table.find_all('td', class_=f'schedule-cell schedule-lesson-type-{digit}')
        for td in div_list:
            td = garb_remove(td.text.strip())
            lessons.append(td)
    dates = [date.text for date in table.find_all('th')]
# lesson_type = []

# for span in span_list: 
#     lesson_type.append(span.text)

for i in lessons: 
    print(i)

print(dates)



