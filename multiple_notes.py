from datetime import datetime


# функция обработки текстовых параметров заметки
def input_parameter_processing(input_key, input_value):
    while True:
        if input_key == 'titles':
            return create_titles(input_value)
        else:
            processing_parameter = input(input_value)
            if processing_parameter:
                return processing_parameter
            else:
                print(f'Некоррктный ввод параметра "{input_key}": "{processing_parameter}"',
                      'Пожалуйста, введите данные', sep='\n')


# функция обработки дат заметки
def input_date_processing(input_key, input_value):
    while True:
        processing_date = input(input_value)
        try:
            datetime.strptime(processing_date, '%d-%m-%Y')
        except ValueError:
            print(f'Некорректный формат "{input_key}": "{processing_date}"',
                  'Убедитесь, пожалуйста, что вводите дату в формате день-месяц-год, например: 20-01-2025.')
            continue
        return processing_date


# функция создания заголовков заметки
def create_titles(input_value):
    titles = [input(input_value)]
    while True:
        title = input('Введите заголовок (или оставьте пустым для завершения): ')
        if not title:
            return sorted(set(titles))
        titles.append(title)


# основная функция создания новых заметок
def create_note():
    created_note = dict()
    created_note['id'] = len(notes) + 1
    for key, value in note_sample.items():
        if key not in ['created_date', 'issue_date']:
            created_note[key] = input_parameter_processing(key, value)
        else:
            created_note[key] = input_date_processing(key, value)
    return created_note


# функция удаления заметки по ключу id из списка заметок
def deleting_notes():
    write_notes(notes)
    for delete_id in map(int, input('Введите id удаляемых заметок через запятую: ').replace(' ', '').split(',')):
        for index, note in enumerate(notes):
            if note['id'] == delete_id:
                del notes[index]


# функция вывода списка заметок
def write_notes(print_notes):
    print('Текущий список заметок:')
    for note in print_notes:
        for key, value in note.items():
            print(f'{note_parameters[key]}: {value}')
        print()


# инициализация параметров
notes = list()
# шаблон заметок
note_sample = {
    'titles': 'Заголовок заметки: ',
    'content': 'Описание заметки: ',
    'status': 'Статус заметки: ',
    'created_date': "Дата создания заметки в формате 'ДД-ММ-ГГГГ': ",
    'issue_date': "Дата истечения заметки в формате 'ДД-ММ-ГГГГ': "
}
# параметры заметок для перевода в человекочитамый вид
note_parameters = {
    'id': 'id',
    'titles': 'Заголовки',
    'content': 'Описание',
    'status': 'Статус',
    'created_date': 'Дата создания',
    'issue_date': 'Дата дедлайна'
}


# начало выполнения программы
username = input_parameter_processing('username', 'Имя пользователя: ')
print('Добро пожаловать в "Менеджер заметок".',
      f'{username}, Вы можете добавить новую заметку.', sep='\n')
# управляющая панель программы
while True:
    notes.append(create_note())
    print('Заметка успешно добавлена!', '\n')
    write_notes(notes)
    if (input(f'{username}, хотите добавить ещё одну заметку? (да/нет): ')).lower() == 'да':
        continue
    if (input(f'{username}, хотите удалить заметку? (да/нет): ')).lower() == 'да':
        deleting_notes()
        continue
    break
print('Готово\n')
print('Пользователь:', username)
write_notes(notes)
