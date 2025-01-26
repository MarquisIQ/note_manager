# функция загрузки заметок из файла
def load_notes_from_file(filename):
    try:
        with open(file=filename, mode='r', encoding='utf-8') as file:
            file.read()
    except FileNotFoundError:
        open(file=filename, mode='x+', encoding='utf-8')
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

    with open(file=filename, mode='r', encoding='utf-8') as file:
        global notes
        new_notes = list()
        note_read = dict()
        for string_index, reading_line in enumerate([line for line in map(
                lambda raw_line: raw_line.replace('\n', ''), file.readlines()) if line]):
            if reading_line.startswith('Список заметок:'):
                continue
            for field in note_fields:
                match field:
                    case 'id':
                        if reading_line.startswith(note_fields[field]):
                            note_read[field] = int((reading_line.replace(f'{note_fields[field]} №', ''))[:-1])
                            break
                    case 'status':
                        if reading_line.startswith(note_fields[field]):
                            status_read = reading_line.replace(f'{note_fields[field]}: ', '')
                            for note_status in note_statuses:
                                if status_read == note_statuses[note_status]:
                                    note_read[field] = note_status
                                    break
                    case 'title':
                        if reading_line.startswith(note_fields[field]):
                            title_read = reading_line.replace(note_fields[field] + ': ', '')
                            note_read[field] = title_read.split(', ')
                            break
                    case _:
                        if reading_line.startswith(note_fields[field]):
                            note_read[field] = reading_line.replace(note_fields[field] + ': ', '')
                            break

            if not note_read:
                print(f'Ошибка валидации файла {filename} в строке {string_index + 1} со значением {reading_line}')
                if input(f'Продолжить выполнение программы? (да/нет): ').lower() == 'нет':
                    return
            elif len(note_read) == len(note_fields):
                new_notes.append(note_read.copy())
                note_read.clear()

    if not new_notes:
        print(f'Файл {filename} пустой')
        return
    notes = new_notes[:]
    return new_notes


# инициализация пользовательских параметров
notes = [{
    'id': 1,
    'username': 'user1',
    'title': ['task1', 'task0'],
    'content': 'content1',
    'status': 'new',
    'created_date': '24-01-2024',
    'issue_date': '24-02-2024'
    }]

# шаблон статусов заметок
note_statuses = {
    'new': 'Новая',
    'in_process': 'В процессе',
    'completed': 'Завершено'
}

note_fields = {
    'id': 'Заметка',
    'username': 'Имя пользователя',
    'title': 'Заголовок',
    'content': 'Описание',
    'status': 'Статус',
    'created_date': 'Дата создания',
    'issue_date': 'Дедлайн'
}

print(load_notes_from_file('example.txt'))
