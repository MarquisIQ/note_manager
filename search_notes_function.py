# функция поиска заметок по ключевым словам и/или статусу
def search_notes(notes, keywords=None, status=None):
    if not notes:
        print('У вас нет сохранённых заметок.')
    else:
        funded_notes = notes[:]
        if status:
            status = status.lower()
            for note_status in note_statuses:
                if note_statuses[note_status].lower() == status:
                    status = note_status
            funded_notes = searching_on_status(funded_notes, status)
        if keywords:
            funded_notes = searching_on_keyword(funded_notes, keywords)
        print('Найдены заметки:')
        display_notes(funded_notes)


# функция поиска по статусу
def searching_on_status(notes, status):
    return [note for note in notes if note['status'] == status]


# функция поиска по ключевым словам
def searching_on_keyword(notes, keywords):
    notes_with_keyword = list()
    for keyword in keywords:
        for note in notes:
            for field in note:
                if field in searching_fields and field == 'title' and len(field) > 1:
                    for title in note[field]:
                        if title == keyword:
                            notes_with_keyword.append(note)
                            break
                        elif keyword in map(str.lower, title.split(' ')):
                            notes_with_keyword.append(note)
                            break
                elif field in searching_fields:
                    if note[field] == keyword:
                        notes_with_keyword.append(note)
                        break
                    elif keyword in note[field].split(' '):
                        notes_with_keyword.append(note)
                        break

    return notes_with_keyword


# функция вывода заметок
def display_notes(output_notes):
    for displayed_note in output_notes:
        for displayed_field in displayed_note:
            match displayed_field:
                case 'id':
                    print(f'{note_fields[displayed_field]} №{displayed_note[displayed_field]}: ')
                case 'title':
                    print(f'{note_fields[displayed_field]}: ', end=' ')
                    print(*displayed_note[displayed_field], sep=', ')
                case 'status':
                    print(f'{note_fields[displayed_field]}: {note_statuses[displayed_note[displayed_field]]}')
                case _:
                    print(f'{note_fields[displayed_field]}: {displayed_note[displayed_field]}')
        print('-' * 30)


# основная функция установки поисковых фильтров и запуска поиска
def select_searching_filters():
    print('Добро пожаловать в поисковик сохраненных заметок!', '\n')
    searching_filters = dict()
    while True:
        print('Доступные критерии для поиска:', *map(lambda x: f'{x + 1}. {list(sample_searching_filters.values())[x]}',
                                                     range(len(sample_searching_filters))), sep='\n')
        searching_filters = select_searching_filter(searching_filters)
        if input('Хотите изменить фильтры? (да/нет): ').lower() == 'да':
            continue
        print('Актуальный список критериев поиска:',
              *map(lambda x: f'{sample_searching_filters[x]}: "{searching_filters[x]}"', searching_filters), sep='\n')
        if input('Запустить поиск? (да/нет): ').lower() == 'да':
            print()
            search_notes(notes, **searching_filters)


# функция выбора доступного фильтра
def select_searching_filter(searching_filters):
    searching_filter = answer_processing(list(sample_searching_filters.values()),
                                         'Выберите критерий для поиска заметок: ')
    if searching_filter in sample_searching_filters.values():
        if searching_filter == sample_searching_filters['status']:
            searching_filters['status'] = select_searching_status()
        else:
            if searching_filter in sample_searching_filters.values():
                for sample_searching_filter in sample_searching_filters:
                    if searching_filter == sample_searching_filters[sample_searching_filter]:
                        received_answer = answer_processing(
                            output_text=searching_filter + ' (через запятую): ')
                        searching_filters[sample_searching_filter] = received_answer.replace(' ', '').split(',')
    return searching_filters


# функция отображения доступных для поиска статусов и выбора искомого
def select_searching_status():
    print('Доступные статусы заметок для поиска:', *map(lambda key: f'{key[0] + 1}. {note_statuses[key[1]]}',
                                                        enumerate(note_statuses.keys())), sep='\n')
    return answer_processing(list(note_statuses.values()), 'Выберите критерий для поиска заметок: ')


# функция-обработчик ответов по вариантам пользователя
def answer_processing(answer_variables=None, output_text=None):
    if not output_text:
        output_text = 'Выберите вариант ответа: '
    while True:
        answer = input(output_text)
        if answer:
            if not answer_variables:
                return answer
            else:
                try:
                    if int(answer) > 0:
                        answer = answer_variables[int(answer) - 1]
                except ValueError:
                    pass
                except IndexError:
                    print('Некорректное значение!')
                    continue

                if answer in answer_variables:
                    return answer
                print('Некорректное значение!')
        else:
            print('Некорректное значение!')



# инициализация пользовательских параметров
notes = [{
    'id': '1',
    'username': 'user1',
    'title': ['task1', 'task0', 'target test'],
    'content': 'content1',
    'status': 'new',
    'created_date': '24-01-2024',
    'issue_date': '24-02-2024'
    },
    {
    'id': '2',
    'username': 'user2',
    'title': ['task2', 'target'],
    'content': 'content2',
    'status': 'in_process',
    'created_date': '24-01-2000',
    'issue_date': '24-02-2024'
    },
    {
    'id': '3',
    'username': 'user3',
    'title': ['task3'],
    'content': 'sex',
    'status': 'in_process',
    'created_date': '24-01-2010',
    'issue_date': '24-02-2020'
    },
    {
    'id': '4',
    'username': 'target',
    'title': ['task2'],
    'content': 'content3',
    'status': 'completed',
    'created_date': '24-01-2020',
    'issue_date': '24-02-2000'
    },
    {
    'id': '5',
    'username': 'user007',
    'title': ['target'],
    'content': 'content7',
    'status': 'new',
    'created_date': '24-01-2020',
    'issue_date': '24-02-2000'
    }]

# поля заметок для перевода в человекочитамый вид
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
    'completed': 'Выполнено'
}

# доступные поля для поиска
searching_fields = ['title', 'content', 'username']

# человекочитаемые значения фильтров
sample_searching_filters = {
    'keywords': 'Ключевые слова',
    'status': 'Статус'
}

# запуск сценария
select_searching_filters()