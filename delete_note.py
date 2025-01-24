# функция вывода текущих заметок
def write_notes(print_notes):
    print('Текущий список заметок:')
    for note in print_notes:
        for key, value in note.items():
            print(f'{note_parameters[key]}: {value}')
        print()


# функция выбора доступного фильтра для удаления
def select_deleting_filter():
    print('Доступные фильтры для удаления:', *map(lambda x: f'{x[0]}. {x[1]}', deleting_filters.items()), sep='\n')
    while True:
        deleting_filter = input('Выберите критерий для удаления заметок: ')
        if deleting_filter in ['username', 'title']:
            return deleting_filter
        elif deleting_filter in ['1', '2']:
            return deleting_filters[deleting_filter]
        print('Некорректное значение', 'Пожалуйста, выберете критерий из списка:',
              *map(lambda x: f'{x[0]}. {x[1]}', deleting_filters.items()), sep='\n')


# функция выбора доступных вариантов для удаления по фильтру
def select_deleting_variables(deleting_filter):
    print(f'Варианты удаления заметок по параметру "{deleting_filter}":')
    deleting_variables = [note[deleting_filter] for note in notes]
    if not all(deleting_variables):
        return None
    unique_deleting_variables = None
    if deleting_filter == 'titles':
        deleting_titles = list()
        for variable in deleting_variables:
            deleting_titles.extend(variable)
            unique_deleting_variables = sorted(set(map(str.lower, deleting_titles)))
    else:
        unique_deleting_variables = sorted(set(map(str.lower, deleting_variables)))
    deleting_indexes = range(len(unique_deleting_variables))
    while True:
        print(*map(lambda x: f'{x + 1}. {unique_deleting_variables[x]}', deleting_indexes), sep='\n')
        deleting_solution = input('Выберите доступный вариант для удаления заметок: ')
        if deleting_solution in unique_deleting_variables:
            return deleting_solution
        elif deleting_solution in map(str, range(1, len(unique_deleting_variables) + 1)):
            return unique_deleting_variables[int(deleting_solution) - 1]
        print('Некорректное значение!', 'Пожалуйста, выберите вариант из списка:', sep='\n')


# основная функция удаления заметок
def deleting_notes():
    deleting_filter = select_deleting_filter()
    deleting_solution = select_deleting_variables(deleting_filter)
    if not deleting_solution:
        print('Параметр отсутствует')
        return None
    deleting_indexes = list()
    for index, note in enumerate(notes):
        if deleting_filter == 'titles':
            for title in note[deleting_filter]:
                if title == deleting_solution:
                    deleting_indexes.append(index)
                    break
        if note.get(deleting_filter) == deleting_solution:
            deleting_indexes.append(index)
    for index in deleting_indexes:
        if input(f"Вы действительно хотите удалить заметку с id {notes[index]['id']} (да/нет): ").lower() == 'нет':
            continue
        del notes[index]
    print('Удаление завершено')
    write_notes(notes)


# инициализация пользовательских данных
notes = [{
    'id': '1',
    'username': 'user1',
    'titles': ['task1'],
    'content': 'content1',
    'status': 'new',
    'created_date': '24-01-2024',
    'issue_date': '24-02-2024'
    },
    {
    'id': '2',
    'username': 'user2',
    'titles': ['task2'],
    'content': 'content2',
    'status': 'in_process',
    'created_date': '24-01-2024',
    'issue_date': '24-02-2024'
    },
    {
    'id': '3',
    'username': 'user3',
    'titles': ['task3'],
    'content': 'content3',
    'status': 'completed',
    'created_date': '24-01-2024',
    'issue_date': '24-02-2024'
    },
    {
    'id': '4',
    'username': 'user1',
    'titles': ['task2'],
    'content': 'content3',
    'status': 'completed',
    'created_date': '24-01-2024',
    'issue_date': '24-02-2024'
    }]

# параметры заметок для перевода в человекочитамый вид
note_parameters = {
    'id': 'id',
    'username': 'Пользователь',
    'titles': 'Заголовки',
    'content': 'Описание',
    'status': 'Статус',
    'created_date': 'Дата создания',
    'issue_date': 'Дата дедлайна'
}

# фильтры доступные для удаления
deleting_filters = {
    '1': 'username',
    '2': 'titles'
}

# запуск основной функции удаления заметок
deleting_notes()
