#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from datetime import date
import json
import sys
import jsonschema


def add():
    # Запросить данные о работнике.
    name = input("Фамилия и инициалы? ")
    groop = input("Группа? ")
    marks = []
    marks = [
        int(i) for i in input("Введите оценки по 5 предметам через пробел: ").split()
    ]

    # Создать словарь.
    return {
        "name": name,
        "groop": groop,
        "marks": marks,
    }


def help():
    # Вывести справку о работе с программой.
    print("Список команд:\n")
    print("add - добавить работника;")
    print("list - вывод студентов с оценками 4 и 5;")
    print("help - отобразить справку;")
    print("exit - завершить работу с программой.")
    year = date.today().year
    print(year)


def list(students):
    # Заголовок таблицы.
    line = "+-{}-+-{}-+-{}-+".format("-" * 30, "-" * 20, "-" * 9)
    print(line)
    print("| {:^30} | {:^20} | {:^9} |".format("Ф.И.О.", "Группа", "Оценки"))
    print(line)

    # Вывести данные о всех студентах.
    for idx, student in enumerate(students, 1):
        print(
            "| {:<30} | {:<20} | {:>7} |".format(
                student.get("name", ""),
                student.get("groop", ""),
                ",".join(map(str, student["marks"])),
            )
        )
    print(line)


def select(students):
    result = []
    for idx, student in enumerate(students, 1):
        res = all(int(x) > 3 for x in student["marks"])
        if res:
            result.append(student)
    return result


def save_students(file_name, students):
    with open(file_name, "w", encoding="utf-8") as fout:
        json.dump(students, fout, ensure_ascii=False, indent=4)


def load_students(file_name):
    schema = {
        "type": "array",
        "items": [
            {
                "type": "object",
                "students": {
                    "name": {"type": "string"},
                    "groop": {"type": "string"},
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
                "required": ["name", "groop", "marks"],
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
    # Список работников.
    students = []

    # Организовать бесконечный цикл запроса команд.
    while True:
        # Запросить команду из терминала.
        command = input(">>> ").lower()

        # Выполнить действие в соответствие с командой.
        if command == "exit":
            break

        elif command == "add":
            student = add()
            # Добавить словарь в список.
            students.append(student)
            # Отсортировать список в случае необходимости.
            if len(students) > 1:
                students.sort(
                    key=lambda item: sum(student["marks"]) / len(student["marks"])
                )

        elif command == "list":
            list(students)

        elif command == "select":
            list(select(students))

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

        elif command == "help":
            help()
        else:
            print(f"Неизвестная команда {command}", file=sys.stderr)


if __name__ == "__main__":
    main()