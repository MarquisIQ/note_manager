def save_notes_to_file(notes, filename):
    writing_notes = notes[:]

    for i, note in enumerate(writing_notes):
        formatted_note = writing_notes[i].copy()
        if len(formatted_note['title']) > 1:
            formatted_note['title'] = ', '.join(note['title'])
            writing_notes[i] = formatted_note
        else:
            formatted_note['title'] = writing_notes[i]['title'][0]
            writing_notes[i] = formatted_note

    with open(file=filename, mode='w', encoding='utf-8') as file:
        file.write('Список заметок:\n\n')
        for note in writing_notes:
            for field in note:
                match field:
                    case 'id':
                        file.write(f'{note_fields[field]} №{note[field]}:\n')
                    case 'status':
                        file.write(f'{note_fields[field]}: {note_statuses[note[field]]}\n')
                    case _:
                        file.write(f'{note_fields[field]}: {note[field]}\n')
            file.write('\n')
    print(f'Записки успешно записаны в файл {filename}')


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

save_notes_to_file(notes, 'example.txt')