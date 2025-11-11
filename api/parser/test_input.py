from schedule_parser import parse_by_url , convert_date, get_datavalue_by_number


START = 'https://rasp.rsreu.ru/schedule-frame/group?faculty=1&group='
END = '&date='

group = get_datavalue_by_number(input('Введите номер вашей группы: '))
date = convert_date(input('Введите дату в формате xx.xx.xx: '))

print(group)
print(date)

URL = START + group + END + date
print(URL)

print(parse_by_url(URL))