from datetime import datetime


# функция обработки текстовых параметров заметки
def input_parameter_processing(input_key, input_value):
    while True:
        if input_key == 'title':
            return create_titles(input_value)
        elif input_key == 'status':
            return create_status(input_value)
        else:
            processing_parameter = input(input_value)
            if processing_parameter:
                return processing_parameter
            else:
                print(f'Некоррктный ввод параметра "{input_key}": "{processing_parameter}"',
                      'Пожалуйста, введите данные', sep='\n')


# функция обработки дат заметки
def input_date_processing(input_key, input_value):
    if input_key == 'created_date':
        return get_current_date()
    while True:
        processing_date = input(input_value)
        try:
            datetime.strptime(processing_date, '%d-%m-%Y')
        except ValueError:
            print(f'Некорректный формат "{input_key}": "{processing_date}"',
                  'Убедитесь, пожалуйста, что вводите дату в формате день-месяц-год, например: 20-01-2025.')
            continue
        return processing_date


# функция получения текущей даты
def get_current_date():
    return datetime.today().strftime('%d-%m-%Y')


# функция создания заголовков заметки
def create_titles(input_value):
    titles = [input(input_value)]
    while True:
        title = input('Введите заголовок (или оставьте пустым для завершения): ')
        if not title:
            return sorted(set(titles))
        titles.append(title)


# функция создания статуса заметки
def create_status(input_value):
    available_statuses = list(note_statuses.values())
    status_indexes = range(len(available_statuses))
    while True:
        print('Доступные статусы заметок:', *map(lambda x: f'{x + 1}. {available_statuses[x]}', status_indexes), sep='\n')
        status = input(input_value)
        if status in available_statuses:
            for note_status in note_statuses:
                if note_statuses[note_status] == status:
                    return note_status
        elif status in map(str, range(1, len(available_statuses) + 1)):
            for note_status in note_statuses:
                if note_statuses[note_status] == available_statuses[int(status) - 1]:
                    return note_status
        else:
            print('Некорректное значение!')


# основная функция создания заметок
def create_note():
    created_note = dict()
    created_note['id'] = len(notes) + 1
    for key, value in note_sample.items():
        if key not in ['created_date', 'issue_date']:
            created_note[key] = input_parameter_processing(key, value)
        else:
            created_note[key] = input_date_processing(key, value)
    return created_note


# инициализация параметров
notes = list()
# шаблон заметок
note_sample = {
    'username': 'Имя пользователя: ',
    'title': 'Заголовок заметки: ',
    'content': 'Описание заметки: ',
    'status': 'Статус заметки: ',
    'created_date': "Дата создания заметки в формате 'ДД-ММ-ГГГГ': ",
    'issue_date': "Дата истечения заметки в формате 'ДД-ММ-ГГГГ': "
}
# шаблон статусов заметок
note_statuses = {
    'new': 'Новая',
    'in_process': 'В процессе',
    'finished': 'Завершено'
}

# запуск создания заметки
print(create_note())
