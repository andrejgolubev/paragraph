from schedule_parser import parse_schedule_from_url , get_datavalue_by_number

PREFIX = 'https://rasp.rsreu.ru/schedule-frame/group?faculty=1&group='

group = get_datavalue_by_number(input('Введите номер вашей группы: '))
date = input('Введите дату в формате xxxx-xx-xx: ')

print(group)
print(date)

URL = PREFIX + group + '&date=' + date
print(URL)


print(parse_schedule_from_url(URL))