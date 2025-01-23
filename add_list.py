username = input("Имя пользователя: ")
first_title = input('Первый заголовок заметки: ')
second_title = input('Второй заголовок заметки: ')
third_title = input('Третий заголовок заметки: ')
content = input('Описание заметки: ')
status = input('Статус заметки: ')
created_date = input("Дата создания заметки в формате 'ДД-ММ-ГГГГ': ")
issue_date = input("Дата истечения заметки в формате 'ДД-ММ-ГГГГ': ")

title = [first_title, second_title, third_title]

print("Имя пользователя:", username)
print('Заголовки заметки', title)
print('Описание заметки', content)
print('Статус заметки', status)
print('Дата создания заметки', created_date)
print('Дата истечения заметки', issue_date)
