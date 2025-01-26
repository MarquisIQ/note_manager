from datetime import datetime
from tabulate import tabulate


# функция создания списка с вариантами ответов
def create_answer_variants(variants, mapping_variants=None):
    processed_variants = ''
    if mapping_variants:
        if type(variants) == list:
            for index in range(len(variants)):
                processed_variants += f'{index + 1}. {mapping_variants[variants[index]]}\n'
        elif type(variants) == dict:
            for index, key in enumerate(variants.keys()):
                processed_variants += f'{index + 1}. {mapping_variants[variants[key]]}\n'
    else:
        if type(variants) == list:
            for index in range(len(variants)):
                processed_variants += f'{index + 1}. {variants[index]}\n'
        elif type(variants) == dict:
            for index, key in enumerate(variants.keys()):
                processed_variants += f'{index + 1}. {variants[key]}\n'
    return processed_variants[:-1]


# функция обработки выбора варианта из списка
def answer_processing(answer_variables=None, output_text=None):
    if not output_text:
        output_text = 'Пожалуйста выберите вариант из списка: '
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
                print(f'Некорректный ввод параметра "{input_key}": "{processing_parameter}"',
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
    print('Доступные статусы заметок:')
    print(create_answer_variants(variants=note_statuses))
    selected_status = answer_processing(answer_variables=list(note_statuses.values()), output_text=input_value)
    for note_status in note_statuses:
        if note_statuses[note_status] == selected_status:
            return note_status


# основная функция создания заметок
def create_note():
    created_note = dict()
    created_note['id'] = len(notes) + 1
    for key, value in note_sample.items():
        if key not in note_dates_fields:
            created_note[key] = input_parameter_processing(key, value)
        else:
            created_note[key] = input_date_processing(key, value)
    notes.append(created_note)
    print('Заметка добавлена:')
    display_notes(displayed_notes=[created_note], select_sorting=False)


# функция вывода заметок
def display_notes(displayed_notes=None, select_sorting=True):
    if not notes:
        print('У вас нет сохранённых заметок.')
    else:
        if not displayed_notes:
            displayed_notes = notes[:]
        if select_sorting:
            if input('Настроить параметры отображения заметок? (да/нет): ').lower() == 'да':
                sorting_parameters = select_sorting_parameters()
            else:
                sorting_parameters = sample_display_parameters
        else:
            sorting_parameters = sample_display_parameters

        if sorting_parameters['sorting_option']:
            displayed_notes = sorting_notes(displayed_notes, **sorting_parameters)

        if not sorting_parameters['full_data']:
            displayed_notes = [{key: value for key, value in note.items() if key == 'title'} for note in displayed_notes]

        for i, note in enumerate(displayed_notes):
            formatted_note = displayed_notes[i].copy()
            if len(formatted_note['title']) > 1:
                formatted_note['title'] = ', '.join(note['title'])
                displayed_notes[i] = formatted_note
            else:
                formatted_note['title'] = displayed_notes[i]['title'][0]
                displayed_notes[i] = formatted_note

        print('Список заметок:', '-' * 30, sep='\n')
        if sorting_parameters['table_view']:
            table_headers = list(map(lambda x: note_fields[x], displayed_notes[0].keys()))
            table_data = list()
            for note in displayed_notes:
                for field in note:
                    if field == 'status':
                        note[field] = note_statuses[note[field]]
                        break
                table_data.append(note.values())
            print(tabulate(headers=table_headers, tabular_data=table_data, tablefmt='orgtbl'))
        else:
            for displayed_note in displayed_notes:
                for displayed_field in displayed_note:
                    match displayed_field:
                        case 'id':
                            print(f'{note_fields[displayed_field]} №{displayed_note[displayed_field]}: ')
                        case 'status':
                            print(f'{note_fields[displayed_field]}: {note_statuses[displayed_note[displayed_field]]}')
                        case _:
                            print(f'{note_fields[displayed_field]}: {displayed_note[displayed_field]}')
                print('-' * 30)
    print()


# функция выбора параметров сортировки
def select_sorting_parameters():
    display_parameters = sample_display_parameters.copy()
    display_parameters['full_data'] = get_answer('Отобразить все данные по заметкам?')
    display_parameters['table_view'] = get_answer('Отобразить в табличном представлении?')
    display_parameters['custom_sorting'] = get_answer('Выбрать режим сортировки заметок?')
    if display_parameters['custom_sorting']:
        display_parameters['sorting_option'] = select_sorting_field()
        display_parameters['sorting_reverse'] = get_answer('Отобразить в обратном порядке?')
    return display_parameters


# функция выбора поля для сортировки
def select_sorting_field():
    while True:
        print('Доступные поля для сортировки: ')
        print(create_answer_variants(variants=note_dates_fields, mapping_variants=note_fields))
        selected_field = answer_processing(answer_variables=list(map(lambda x: note_fields[x], note_dates_fields)),
                                           output_text='Выберите режим сортировки: ')
        for field in note_fields:
            if note_fields[field] == selected_field:
                return field


# функция сортировки заметок
def sorting_notes(selected_notes, **sorting_parameters):
    sorted_notes = selected_notes[:]
    return sorted(sorted_notes,
                  key=lambda note: datetime.strptime(note[sorting_parameters['sorting_option']], '%d-%m-%Y'),
                  reverse=sorting_parameters['sorting_reverse'])


# функция обработки ответов пользователя
def get_answer(question):
    while True:
        answer = input(f'{question} (да/нет): ').lower()
        if answer == 'да':
            return True
        elif answer == 'нет':
            return False
        print('Некорректный ввод!')


# функция обновления полей в заметке
def update_field(selected_note, field):
    edited_note = notes[selected_note].copy()
    output_sample = 'Вы действительно хотите изменить выбранное значение:'
    updating_value = note_statuses[edited_note[field]] if field == 'status' else edited_note[field]
    print(f'{output_sample} "{updating_value}" для поля: "{note_fields[field]}"', f'в заметке №{edited_note["id"]}?', sep=' ', end=' ')
    if input('(да/нет): ').lower() != 'нет':
        if field == 'status':
            notes[selected_note][field] = create_status('Выберите статус или оставьте поле пустым для отмены: ')
        elif field in note_dates_fields:
            new_date = input_date_processing(field, note_sample[field] + ' или оставьте поле пустым для отмены: ')
            if new_date:
                notes[selected_note][field] = new_date
        else:
            new_value = input('Введите новое значение или оставьте поле пустым для отмены: ')
            if new_value:
                notes[selected_note][field] = new_value
    print('Обновление заметки завершено!\n')
    return edited_note


# основная функция изменения заметки
def update_note():
    display_notes(select_sorting=False)
    selected_note = int(answer_processing(answer_variables=[i['id'] for i in notes],
                                          output_text='Выберите номер заметки для обновления: ')) - 1
    print('Список доступных полей для изменения:')
    print(create_answer_variants(variants=list(note_fields.values())[1:]))
    solution = answer_processing(answer_variables=list(note_fields.values())[1:])

    for field in note_fields:
        if note_fields[field] == solution:
            return update_field(selected_note, field)


# основная функция удаления заметок
def delete_note():
    deleting_filter = select_deleting_filter()
    deleting_solution = select_deleting_variables(deleting_filter)
    if not deleting_solution:
        print('Параметр отсутствует')
        return None
    deleting_ids = list()
    for note in notes:
        if deleting_filter == 'title':
            for title in note[deleting_filter]:
                if title == deleting_solution:
                    deleting_ids.append(note['id'])
                    break
        if note.get(deleting_filter) == deleting_solution:
            deleting_ids.append(note['id'])
    for note in notes:
        if note['id'] in deleting_ids:
            if input(f"Вы действительно хотите удалить заметку №{note['id']}? (да/нет): ").lower() == 'нет':
                continue
            del notes[note['id'] - 1]
    print('Удаление завершено\n')
    for i, note in enumerate(notes):
        note['id'] = i + 1
    display_notes(select_sorting=False)


# функция выбора доступного фильтра для удаления
def select_deleting_filter():
    print('Доступные фильтры для удаления:')
    print(create_answer_variants(variants=deleting_filters, mapping_variants=note_fields))
    selected_filter = answer_processing(answer_variables=list(map(lambda x: note_fields[x], deleting_filters)))
    for deleting_filter in deleting_filters:
        if note_fields[deleting_filter] == selected_filter:
            return deleting_filter


# функция выбора доступных вариантов для удаления по фильтру
def select_deleting_variables(deleting_filter):
    print(f'Варианты удаления заметок по параметру "{deleting_filter}":')
    deleting_variables = [note[deleting_filter] for note in notes]
    if not all(deleting_variables):
        return None
    unique_deleting_variables = None
    if deleting_filter == 'title':
        deleting_titles = list()
        for variable in deleting_variables:
            deleting_titles.extend(variable)
            unique_deleting_variables = sorted(set(map(str.lower, deleting_titles)))
    else:
        unique_deleting_variables = sorted(set(map(str.lower, deleting_variables)))
    while True:
        print(create_answer_variants(variants=unique_deleting_variables))
        deleting_solution = input('Выберите доступный вариант для удаления заметок: ')
        if deleting_solution in unique_deleting_variables:
            return deleting_solution
        elif deleting_solution in map(str, range(1, len(unique_deleting_variables) + 1)):
            return unique_deleting_variables[int(deleting_solution) - 1]
        print('Некорректное значение!', 'Пожалуйста, выберите вариант из списка:', sep='\n')


# функция поиска заметок по ключевым словам и/или статусу
def find_notes():
    if not notes:
        print('У вас нет сохранённых заметок.')
    else:
        searching_filters = dict()
        while True:
            print('Доступные критерии для поиска:')
            print(create_answer_variants(variants=sample_searching_filters))
            searching_filters = select_searching_filter(searching_filters)
            if input('Хотите изменить фильтры? (да/нет): ').lower() == 'да':
                continue
            print('Актуальный список критериев поиска:')
            print(*map(lambda x: f'{sample_searching_filters[x]}: "{searching_filters[x]}"', searching_filters), sep='\n')
            if input('Запустить поиск? (да/нет): ').lower() == 'да':
                funded_notes = notes[:]

                if searching_filters.get('status'):
                    for note_status in note_statuses:
                        if note_statuses[note_status] == searching_filters['status']:
                            funded_notes = [note for note in notes if note['status'] == note_status]
                            break

                if searching_filters.get('keywords'):
                    funded_notes = searching_on_keywords(funded_notes, searching_filters['keywords'])
                print(f'По указанным фильтрам найдено записей: {len(funded_notes)}')
                if funded_notes:
                    display_notes(displayed_notes=funded_notes)
                else:
                    print()
                break


# функция поиска по ключевым словам
def searching_on_keywords(select_notes, keywords):
    notes_with_keyword = list()
    for keyword in keywords:
        for note in select_notes:
            for field in note:
                if field == 'title':
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
                        received_answer = answer_processing(output_text=searching_filter + ' (через запятую): ')
                        searching_filters[sample_searching_filter] = received_answer.lower().replace(' ', '').split(',')
    return searching_filters


# функция отображения доступных для поиска статусов и выбора искомого
def select_searching_status():
    print('Доступные статусы заметок для поиска:')
    print(create_answer_variants(variants=note_statuses))
    return answer_processing(list(note_statuses.values()), 'Выберите критерий для поиска заметок: ')


# функция выхода из меню
def exit_menu():
    return 'stop'


# основная функция генерации меню действий
def menu():
    while True:
        selected_action = None
        print('Меню действий:')
        print(create_answer_variants(variants=menu_parameters))
        action = answer_processing(answer_variables=list(menu_parameters.values()),
                                   output_text='Пожалуйста, выберите действие из меню: ')
        for menu_parameter in menu_parameters:
            if menu_parameters[menu_parameter] == action:
                selected_action = menu_parameter
                break
        result_action = selected_action()

        if result_action == 'stop':
            print('Программа завершена. Спасибо за использование!')
            break


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

# шаблон заметок
note_sample = {
    'username': 'Имя пользователя: ',
    'title': 'Заголовок заметки: ',
    'content': 'Описание заметки: ',
    'status': 'Статус заметки: ',
    'created_date': "Дата создания заметки в формате 'ДД-ММ-ГГГГ': ",
    'issue_date': "Дата истечения заметки в формате 'ДД-ММ-ГГГГ': "
}

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

# параметры отображения по умолчанию
sample_display_parameters = {
    'full_data': True,
    'table_view': True,
    'custom_sorting': False,
    'sorting_option': 'created_date',
    'sorting_reverse': False
}

# шаблон статусов заметок
note_statuses = {
    'new': 'Новая',
    'in_process': 'В процессе',
    'completed': 'Завершено'
}

# поля заметок с датами
note_dates_fields = ['created_date', 'issue_date']

# фильтры доступные для удаления
deleting_filters = ['username', 'title']

# доступные поля для поиска
searching_fields = ['title', 'content', 'username']

# человекочитаемые значения фильтров
sample_searching_filters = {
    'keywords': 'Ключевые слова',
    'status': 'Статус'
}

# доступные действия меню
menu_parameters = {
    create_note: 'Создать новую заметку',
    display_notes: 'Показать все заметки',
    update_note: 'Обновить заметку',
    delete_note: 'Удалить заметку',
    find_notes: 'Найти заметки',
    exit_menu: 'Выйти из программы'
}

# запуск программы
print('Добро пожаловать в приложение "Менеджер заметок"!\n')
menu()