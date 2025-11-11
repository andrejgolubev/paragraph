from utils.utils import groups
import requests 
#построение уникальной ссылки по запросу юзера. с этой ссылки будет парсится таблица с расписанием и отображаться. 
# кстати абсолютно пох какая тут будет digit в faculty, их сайт выдаёт инфу при любой 
# (сам проверь, выбрав группу и потом в URLe меняя faculty )
url = f'https://rasp.rsreu.ru/schedule-frame/group?faculty=1&group={groups['5413']}&date='

print(url)