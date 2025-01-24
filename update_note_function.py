from datetime import datetime


# функция обновления полей в заметке
def update_field(note, field):
    edited_note = note.copy()
    output_sample = 'Вы действительно хотите изменить значение:'
    updating_value = note_statuses[note[field]] if field == 'status' else note[field]
    print(f'{output_sample} "{updating_value}" поля: "{note_fields[field]}"', f'в заметке с id: {note["id"]}?', sep=' ', end=' ')
    if input('(да/нет): ') != 'нет':
        if field == 'status':
            edited_note[field] = create_status(note_sample[field] + ' или оставьте поле пустым для отмены: ')
        elif field in note_dates_fields:
            new_date = input_date_processing(field, note_sample[field] + ' или оставьте поле пустым для отмены: ')
            if new_date:
                edited_note[field] = new_date
        else:
            new_value = input('Введите новое значение или оставьте поле пустым для отмены: ')
            if new_value:
                edited_note[field] = new_value
    return edited_note


# функция обработки дат
def input_date_processing(input_key, input_value):
    while True:
        processing_date = input(input_value)
        if not processing_date:
            return None
        try:
            datetime.strptime(processing_date, '%d-%m-%Y')
        except ValueError:
            print(f'Некорректный формат "{input_key}": "{processing_date}"',
                  'Убедитесь, пожалуйста, что вводите дату в формате день-месяц-год, например: 20-01-2025.')
            continue
        return processing_date


# функция создания статуса заметки
def create_status(input_value):
    available_statuses = list(note_statuses.values())
    while True:
        print('Доступные статусы заметок:', *map(lambda x: f'{x + 1}. {available_statuses[x]}', range(len(available_statuses))), sep='\n')
        status = input(input_value)
        try:
            if int(status) > 0:
                status = available_statuses[int(status) - 1]
            else:
                print(f'Некорректное значение: {status}!')
                continue
        except ValueError:
            pass
        except IndexError:
            print(f'Некорректное значение: {status}!')
            continue
        if status in available_statuses:
            for note_status in note_statuses:
                if note_statuses[note_status] == status:
                    return note_status
        else:
            print('Некорректное значение!')


# основная функция изменения заметки
def update_note(note):
    available_fields = list(note.keys())
    while True:
        print('Список доступных полей для изменения:',
              *map(lambda x: f'{x + 1}. {available_fields[x]}', range(len(available_fields))), sep='\n')
        solution = input('Пожалуйста выберите вариант из списка: ')
        try:
            if int(solution) > 0:
                solution = available_fields[int(solution) - 1]
            else:
                print(f'Некорректное значение: {solution}!')
                continue
        except ValueError:
            pass
        except IndexError:
            print(f'Некорректное значение: {solution}!')
            continue
        if solution in available_fields:
            return update_field(note, solution)
        else:
            print(f'Некорректное значение: {solution}!')


# инициализация пользовательских данных
notes = [{
    'id': '1',
    'username': 'user1',
    'title': ['task1', 'task0'],
    'content': 'content1',
    'status': 'new',
    'created_date': '24-01-2024',
    'issue_date': '24-02-2024'
    },
    {
    'id': '2',
    'username': 'user2',
    'title': ['task2'],
    'content': 'content2',
    'status': 'in_process',
    'created_date': '24-01-2024',
    'issue_date': '24-02-2024'
    },
    {
    'id': '3',
    'username': 'user3',
    'title': ['task3'],
    'content': 'content3',
    'status': 'completed',
    'created_date': '24-01-2024',
    'issue_date': '24-02-2024'
    },
    {
    'id': '4',
    'username': 'user1',
    'title': ['task2'],
    'content': 'content3',
    'status': 'completed',
    'created_date': '24-01-2024',
    'issue_date': '24-02-2024'
    }]

# параметры заметок для перевода в человекочитамый вид
note_fields = {
    'id': 'id',
    'username': 'Пользователь',
    'title': 'Заголовки',
    'content': 'Описание',
    'status': 'Статус',
    'created_date': 'Дата создания',
    'issue_date': 'Дата дедлайна'
}

# шаблон заметок
note_sample = {
    'id': 'id',
    'username': 'Имя пользователя',
    'title': 'Заголовок заметки',
    'content': 'Описание заметки',
    'status': 'Статус заметки',
    'created_date': "Дата создания заметки в формате 'ДД-ММ-ГГГГ'",
    'issue_date': "Дата истечения заметки в формате 'ДД-ММ-ГГГГ'"
}

# шаблон статусов заметок
note_statuses = {
    'new': 'Новая',
    'in_process': 'В процессе',
    'completed': 'Завершено'
}

# поля с датами для валидации ввода дат
note_dates_fields = ['created_date', 'issue_date']

print(update_note(notes[0]))
