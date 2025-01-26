# функция добавления заметок в файл
def append_notes_to_file(notes, filename):
    try:
        with open(file=filename, mode='r', encoding='utf-8'):
            pass
    except FileNotFoundError:
        with open(file=filename, mode='w', encoding='utf-8') as updating_file:
            updating_file.write('Список заметок:\n\n')
            print(f'Файл "{filename}" не найден. Создан новый файл.')
    except UnicodeDecodeError:
        print(f'Произошла ошибка при декодировании файла "{filename}"')
        if input(f'Продолжить выполнение программы? (да/нет): ').lower() == 'нет':
            return
    except PermissionError:
        print(f'Недостаточно прав для чтения файла "{filename}"')
        if input(f'Продолжить выполнение программы? (да/нет): ').lower() == 'нет':
            return
    except Exception as exception:
        print(f'Во время записи в файл {filename} произошла непредвиденная ошибка {exception}')
        if input(f'Продолжить выполнение программы? (да/нет): ').lower() == 'нет':
            return

    try:
        with open(file=filename, mode='a', encoding='utf-8'):
            pass
    except PermissionError:
        print(f'Недостаточно прав для записи в файл "{filename}"')
        if input(f'Продолжить выполнение программы? (да/нет): ').lower() == 'нет':
            return
    except Exception as exception:
        print(f'Во время записи в файл {filename} произошла непредвиденная ошибка {exception}')
        if input(f'Продолжить выполнение программы? (да/нет): ').lower() == 'нет':
            return

    writing_notes = notes[:]
    for i, note in enumerate(writing_notes):
        formatted_note = writing_notes[i].copy()
        if len(formatted_note['title']) > 1:
            formatted_note['title'] = ', '.join(note['title'])
            writing_notes[i] = formatted_note
        else:
            formatted_note['title'] = writing_notes[i]['title'][0]
            writing_notes[i] = formatted_note

    notes_ids = [0]
    with open(file=filename, mode='r', encoding='utf-8') as read_file:
        for reading_line in [line for line in map(
                lambda raw_line: raw_line.replace('\n', ''), read_file.readlines()) if line][1:]:
            if reading_line.startswith(note_fields['id']):
                notes_ids.append(int((reading_line.replace(f'{note_fields['id']} №', ''))[:-1]))

    last_notes_id = max(notes_ids)
    with open(file=filename, mode='a', encoding='utf-8') as update_file:
        for note in writing_notes:
            last_notes_id += 1
            for field in note:
                match field:
                    case 'id':
                        update_file.write(f'{note_fields[field]} №{last_notes_id}:\n')
                    case 'status':
                        update_file.write(f'{note_fields[field]}: {note_statuses[note[field]]}\n')
                    case _:
                        update_file.write(f'{note_fields[field]}: {note[field]}\n')
            update_file.write('\n')
    print(f'Записки успешно добавлены в файл {filename}')


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

# запуск программы
append_notes_to_file(notes, 'example.txt')