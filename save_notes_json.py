import json


# функция сохранения заметок в формате json в файл
def save_notes_json(notes, filename):
    try:
        open(file=filename, mode='x+', encoding='utf-8')
    except FileExistsError:
        if input(f'Вы уверены, что хотите перезаписать файл "{filename}" (да/нет): ').lower() == 'нет':
            return
    except PermissionError:
        print(f'Недостаточно прав для записи в файл "{filename}"')
        if input(f'Продолжить выполнение программы? (да/нет): ').lower() == 'нет':
            return
    except Exception as exception:
        print(f'Во время записи в файл {filename} произошла непредвиденная ошибка {exception}')
        if input(f'Продолжить выполнение программы? (да/нет): ').lower() == 'нет':
            return

    writing_notes = ['List of notes']
    writing_notes.extend(notes)
    with open(file=filename, mode='w', encoding='utf-8') as file:
        file.write(json.dumps(writing_notes, indent=4))
    print(f'Записки в формате json успешно сохранены в файл {filename}')


# инициализация пользовательских параметров
notes = [{
    'id': 1,
    'username': 'user1',
    'title': ['task1', 'task0'],
    'content': 'content1',
    'status': 'new',
    'created_date': '24-01-2024',
    'issue_date': '24-02-2024'
    },
    {
    'id': 2,
    'username': 'user2',
    'title': ['task2'],
    'content': 'content2',
    'status': 'in_process',
    'created_date': '24-01-2000',
    'issue_date': '24-02-2024'
    },
    {
    'id': 3,
    'username': 'user3',
    'title': ['task3'],
    'content': 'content3',
    'status': 'completed',
    'created_date': '24-01-2010',
    'issue_date': '24-02-2020'
    },
    {
    'id': 4,
    'username': 'user1',
    'title': ['task2'],
    'content': 'content3',
    'status': 'completed',
    'created_date': '24-01-2020',
    'issue_date': '24-02-2000'
    }]

# поля заметок для перевода в человекочитаемый формат
note_fields = {
    'id': 'Заметка',
    'username': 'Имя пользователя',
    'title': 'Заголовок',
    'content': 'Описание',
    'status': 'Статус',
    'created_date': 'Дата создания',
    'issue_date': 'Дедлайн'
}

# шаблон статусов заметок
note_statuses = {
    'new': 'Новая',
    'in_process': 'В процессе',
    'completed': 'Завершено'
}

save_notes_json(notes, filename='example.json')