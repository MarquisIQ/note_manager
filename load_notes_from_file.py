def load_notes_from_file(filename):
    try:
        with open(file=filename, mode='r', encoding='utf-8') as file:
            global notes
            notes.clear()
            note_read = dict()
            for reading_line in [line for line in map(
                    lambda raw_line: raw_line.replace('\n', ''), file.readlines()) if line][1:]:
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

                if len(note_read) == len(note_fields) - 1:
                    notes.append(note_read.copy())
                    note_read.clear()

        return notes

    except FileNotFoundError:
        print('Искомый файл не найден!')


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
