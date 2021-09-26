import csv


MENU_OPTIONS = {
    '1': 'Вывести иерархию команд, т.е. департамент и все команды, которые\
входят в него',
    '2': 'Вывести сводный отчёт по департаментам: название, численность, \
"вилка" зарплат, средняя зарплата',
    '3': 'Сохранить сводный отчёт по департаментам в виде csv-файла.'
}
CONTINUE_OPERATION_MENU_OPTIONS = {
    'да': True,
    'нет': False
}


def get_employee_data():
    '''
    Функция считывает данные о сотрудниках из csv-файла в словарь.
    '''
    employee_data = {}
    with open('Corp Summary.csv', newline='') as csvfile:
        datareader = csv.reader(csvfile, delimiter=';')
        for index, row in enumerate(datareader):
            if index == 0:
                keys = row
            if index > 0 and len(row) > 0:
                employee_data[index] = {
                    keys[0]: row[0],
                    keys[1]: row[1],
                    keys[2]: row[2],
                    keys[3]: row[3],
                    keys[4]: float(row[4]),
                    keys[5]: int(row[5])
                }
    return show_menu(employee_data)


def show_menu(employee_data: dict):
    '''
    Функция показывает меню с доступными для выбора задачами.
    '''
    print(
        'Доступные для выполнения задачи:'
    )
    for key in MENU_OPTIONS:
        print(f'{key}: {MENU_OPTIONS[key]}')
    option = ''
    while option not in MENU_OPTIONS:
        print('Выберите: {}, {} или {}.'.format(*MENU_OPTIONS))
        option = input()
        if option == '1':
            print_team_hierarchy(employee_data)
        if option == '2':
            department_salaries = get_department_salaries(employee_data)
            print_department_summary(department_salaries)
        if option == '3':
            department_salaries = get_department_salaries(employee_data)
            save_department_summary_to_csv(department_salaries)

    option = ''
    print('Продолжить работу?')
    while option not in CONTINUE_OPERATION_MENU_OPTIONS:
        print('Выберите: {} или {}.'.format(*CONTINUE_OPERATION_MENU_OPTIONS))
        option = input()
    if CONTINUE_OPERATION_MENU_OPTIONS[option]:
        return show_menu(employee_data)
    else:
        return None


def print_team_hierarchy(employee_data: dict):
    '''
    Функция выводит иерархию команд от департамента к отделам.
    '''
    team_hierarchy = {}
    for value in employee_data.values():
        if value['Департамент'] not in team_hierarchy.keys():
            team_hierarchy[value['Департамент']] = []
        if value['Отдел'] not in team_hierarchy[value['Департамент']]:
            team_hierarchy[value['Департамент']].append(value['Отдел'])
    print('Иерархия команд (департамент, отделы):')
    print()
    for key, value in team_hierarchy.items():
        print(f'{key}')
        for team in value:
            print(f'\t{team}')
        print()
    return None


def get_department_salaries(employee_data: dict):
    '''
    Функция выбирает из общего массива данных о сотрудниках информацию о
    зарплатах в каждом департаменте.
    '''
    department_salaries = {}
    for value in employee_data.values():
        if value['Департамент'] not in department_salaries.keys():
            department_salaries[value['Департамент']] = []
        department_salaries[value['Департамент']].append(value['Оклад'])
    return department_salaries


def print_department_summary(department_salaries: dict):
    '''
    Функция выводит сводный отчет о департаменте.
    '''
    print('Сводный отчет по департаментам:')
    print()
    for key, value in department_salaries.items():
        print(
            f'{key}\n'
            f'\tЧисленность: {len(value)}\n'
            f'\t"Вилка" зарплат: {min(value)} - {max(value)}\n'
            f'\tСредняя зарплата: {sum(value) / len(value):.2f}\n'
        )
    return None


def save_department_summary_to_csv(department_salaries: dict):
    '''
    Функция сохраняет сводный отчет о департаменте в csv-файл.
    '''
    filename = 'Department Summary.csv'
    report_header_fields = (
        'Название',
        'Численность',
        'Вилка зарплат',
        'Средняя зарплата'
    )
    with open(f'./{filename}', 'w') as f:
        out_file = csv.writer(f, delimiter=';')
        out_file.writerow(report_header_fields)
        for key, value in department_salaries.items():
            out_file.writerow((
                key,
                len(value),
                f'{min(value)} - {max(value)}',
                f'{sum(value) / len(value):.2f}'
            ))
    print(f'Отчет сохранен в {filename}')
    return None


if __name__ == '__main__':
    get_employee_data()
