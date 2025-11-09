from datetime import datetime

days_translation = {
        'Monday': 'Понедельник',
        'Tuesday': 'Вторник', 
        'Wednesday': 'Среда',
        'Thursday': 'Четверг',
        'Friday': 'Пятница',
        'Saturday': 'Суббота',
        'Sunday': 'Воскресенье'
    }

def get_dates():
    now = datetime.now() 
    now = now.strftime('%A, %d %B %Y')
    print(now) 

get_date()