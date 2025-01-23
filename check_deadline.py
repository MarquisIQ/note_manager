from datetime import datetime


# Получаем текущую дату
def get_current_date():
    return datetime.today()


# запрашиваем дату дедлайна пока формат не будет верным
def get_deadline_date():
    while True:
        issue_date = input('Введите дату дедлайна в формате "ДД-ММ-ГГГГ": ')
        try:
            return datetime.strptime(issue_date, '%d-%m-%Y')
        except ValueError:
            print(f'Некорректный формат даты "{issue_date}", убедитесь, что вводите дату в формате день-месяц-год, например: 20-01-2025.')


# считаем верное окончание исходя из количества дней
def get_ending(days):
    days = abs(days) % 100
    if 5 <= days <= 20:
        return 'дней'
    days %= 10
    if days == 1:
        return 'день'
    elif 2 <= days <= 4:
        return 'дня'
    else:
        return 'дней'


# переводим строки в даты, считаем разницу и выводим результат
def calc_date_diff():
    date_diff = (get_deadline_date() - get_current_date()).days
    if date_diff > 0:
        return f'До даты дедлайна: {date_diff} {get_ending(date_diff)}'
    elif date_diff < 0:
        return f'Внимание! Дата дедлайна прошла {abs(date_diff)} {get_ending(date_diff)} назад!'
    else:
        return 'Внимание! Дата дедлайна сегодня!'


print('Текущая дата:', datetime.strftime(get_current_date(), '%d-%m-%Y'))
print(calc_date_diff())
