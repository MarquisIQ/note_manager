#создаем словарь статусов и задаем текущий статус
statuses = {'1': 'выполнено', '2': 'в процессе', '3': 'отложено'}
old_status = statuses['3']
print('Текущий статус заметки: ' + old_status)

#в цикле запрашиваем ввод пока не получим один из ключей или знанчений из словаря статусов заметок
while True:
    note_status = input('Введите новый статус заметки: ')
    if note_status in statuses.keys():
        find_in_key = True
        break
    elif note_status in statuses.values():
        find_in_key = False
        break
    print('''
    Неккорректный новый статус заметки, выберите один из предложенных вариантов:
    1 - выполнено,
    2 - в процессе,
    3 - отложено
    ''')

#Выводим новый статус заметки в зависимости от места нахождения введеного значения
print('Новый статус заметки:', (statuses[note_status] if find_in_key else note_status))
