from datetime import datetime
from tabulate import tabulate


# функция вывода заметок
def display_notes(output_notes, sorting_parameters):
    if not output_notes:
        print('У вас нет сохранённых заметок.')
    else:
        if sorting_parameters['sorting_option']:
            output_notes = sorting_notes(output_notes, **sorting_parameters)
        if not sorting_parameters['full_data']:
            displayed_notes = [{key: value for key, value in note.items() if key == 'title'} for note in output_notes]

        else:
            displayed_notes = output_notes
        print('Список заметок:', '-' * 30, sep='\n')
        if sorting_parameters['table_view']:
            table_headers = list(map(lambda x: note_fields[x], displayed_notes[0].keys()))
            table_data = list()
            for i, note in enumerate(displayed_notes):
                displayed_notes[i]['title'] = ', '.join(note['title'])
            for note in displayed_notes:
                table_data.append(note.values())
            print(tabulate(headers=table_headers, tabular_data=table_data, tablefmt='orgtbl'))
        else:
            for displayed_note in displayed_notes:
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


# функция выбора поля для сортировки
def select_sorting_field():
    print('Доступные поля для сортировки: ')
    print(*map(lambda x: f'{x + 1}. {note_fields[sorting_fields[x]]}', range(len(sorting_fields))), sep='\n')
    while True:
        sorting_field = input('Выберите режим сортировки: ')
        try:
            if int(sorting_field) > 0:
                sorting_field = sorting_fields[int(sorting_field) - 1]
            else:
                print('Некорректное значение!')
                continue
        except ValueError:
            pass
        except IndexError:
            print('Некорректное значение!')
            continue
        if sorting_field in sorting_fields:
            return sorting_field


# функция сортировки заметок
def sorting_notes(selected_notes, **sorting_parameters):
    sorted_notes = selected_notes[:]
    return sorted(sorted_notes,
                  key=lambda note: datetime.strptime(note[sorting_parameters['sorting_option']], '%d-%m-%Y'),
                  reverse=sorting_parameters['sorting_reverse'])


# функция обработки ответов пользователя
def get_answer(question):
    while True:
        answer = input(f'{question} (да/нет): ')
        if answer in 'да':
            return True
        elif answer == 'нет':
            return False
        print('Некорректный ввод!')


# инициализация пользовательских параметров
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
    'created_date': '24-01-2000',
    'issue_date': '24-02-2024'
    },
    {
    'id': '3',
    'username': 'user3',
    'title': ['task3'],
    'content': 'content3',
    'status': 'completed',
    'created_date': '24-01-2010',
    'issue_date': '24-02-2020'
    },
    {
    'id': '4',
    'username': 'user1',
    'title': ['task2'],
    'content': 'content3',
    'status': 'completed',
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

# параметры отображения по умолчанию
sample_display_parameters = {
    'full_data': True,
    'table_view': False,
    'custom_sorting': False,
    'sorting_option': False,
    'sorting_reverse': False
}

# доступные поля для сортировки
sorting_fields = ['created_date', 'issue_date']

# шаблон статусов заметок
note_statuses = {
    'new': 'Новая',
    'in_process': 'В процессе',
    'completed': 'Завершено'
}

# запуск программы
display_parameters = sample_display_parameters.copy()
display_parameters['full_data'] = get_answer('Отобразить все данные по заметкам?')
display_parameters['table_view'] = get_answer('Отобразить в табличном представлении?')
display_parameters['custom_sorting'] = get_answer('Выбрать режим сортировки заметок?')
if display_parameters['custom_sorting']:
    display_parameters['sorting_option'] = select_sorting_field()
    display_parameters['sorting_reverse'] = get_answer('Отобразить в обратном порядке?')
display_notes(notes, display_parameters)
