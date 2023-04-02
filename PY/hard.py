#!/usr/bin/env python3
# _*_ coding: utf-8 _*_

import sys
import json
import jsonschema


def get_student(staff):
    """
    Запросить данные о студенте.
    """
    name = input("Фамилия и инициалы? ")
    group = input("Номер группы? ")
    grade = list(map(int, input("введите свои оценки: ").split()))

    # Создать словарь.
    student = {
        'name': name,
        'group': group,
        'grade': grade,
    }
    # Добавить словарь в список.
    staff.append(student)

    # Отсортировать список в случае необходимости.
    if len(staff) > 1:
        staff.sort(key=lambda item: item.get('group')[::-1])


def display_student(staff):
    """
    Отобразить список студентов.
    """
    if staff:
        # Заголовок таблицы.
        line = '+-{}-+-{}-+-{}-+-{}-+'.format(
            '-' * 4,
            '-' * 30,
            '-' * 20,
            '-' * 15
        )
        print(line)
        print(
            '| {:^4} | {:^30} | {:^20} | {:^15} |'.format(
                "№",
                "Ф.И.О.",
                "Группа",
                "Оценки"
            )
        )
        print(line)
        # Вывести данные о всех студентах.
        for idx, student in enumerate(staff, 1):
            print(
                '| {:>4} | {:<30} | {:<20} | {:>15} |'.format(
                    idx,
                    student.get('name', ''),
                    student.get('group', ''),
                    ','.join(map(str, student['grade']))
                )
            )
        print(line)
    else:
        print("список студентов пуст")


def find_students(staff):
    """
    Выбрать студентов со ср ариф. успеваемости >4.
    """
    result = []
    count = 0
    for student in staff:
        grade = student.get('grade', '')
        if sum(grade) / (len(grade)) >= 4.0:
            result.append(student)
            count += 1

    return result


def save_students(file_name, staff):
    with open(file_name, "w", encoding="utf-8") as fout:
        json.dump(staff, fout, ensure_ascii=False, indent=4)


def load_students(file_name):
    schema = {
        "type": "array",
        "items": [
            {
                "type": "object",
                "students": {
                    "name": {"type": "string"},
                    "group": {"type": "string"},
                    "marks": {
                        "type": "array",
                        "items": [
                            {"type": "integer"},
                            {"type": "integer"},
                            {"type": "integer"},
                            {"type": "integer"},
                            {"type": "integer"},
                        ],
                    },
                },
                "required": ["name", "group", "grade"],
            }
        ],
    }
    with open(file_name, "r", encoding="utf-8") as fin:
        loadfile = json.load(fin)
        validator = jsonschema.Draft7Validator(schema)
        try:
            if not validator.validate(loadfile):
                print("Валидация прошла успешно")
        except jsonschema.exceptions.ValidationError:
            print("Ошибка валидации", file=sys.stderr)
            exit()
    return loadfile


def main():
    """
    Главная функция программы.
    """
    students = []

    # Организовать бесконечный цикл запроса команд.
    while True:
        # Запросить команду из терминала.
        command = input(">>> ").lower()

        # Выполнить действие в соответствие с командой.
        if command == 'exit':
            break

        elif command == 'add':
            get_student(students)

        elif command == 'list':
            display_student(students)

        elif command == 'find':
            found = find_students(students)
            display_student(found)

        elif command.startswith("save "):
            # Разбить команду на части для выделения имени файла.
            parts = command.split(maxsplit=1)
            # Получить имя файла.
            file_name = parts[1]
            # Сохранить данные в файл с заданным именем.
            save_students(file_name, students)

        elif command.startswith("load "):
            # Разбить команду на части для выделения имени файла.
            parts = command.split(maxsplit=1)
            # Получить имя файла.
            file_name = parts[1]
            # Сохранить данные в файл с заданным именем.
            students = load_students(file_name)

        elif command == 'help':
            print("Список команд:\n")
            print("add - добавить студента;")
            print("list - вывести список студентов;")
            print("find - вывод на фамилий и номеров групп студента с оценками 4 и 5 ;")
            print("help - отобразить справку;")
            print("load - загрузить данные из файла;")
            print("save - сохранить данные в файл;")
            print("exit - завершить работу с программой.")

        else:
            print(f"Неизвестная команда {command}", file=sys.stderr)


if __name__ == '__main__':
    main()
