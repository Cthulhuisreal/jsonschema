import os
import sys
import jsonschema
import simplejson as json


def valid(inst_path, sch_path):
    """Валидация JSON-файлов при помощи JSON-схем.

    Аргументы:
    inst_path -- путь к папке в JSON-файлами
    sch_path -- путь к папке в JSON-схемами
    """
    # Создаём и открываем файл записи логов скрипта
    sys.stdout = open('logs.txt', 'w')
    # Открываем каждый файл из папки с JSON-файлами
    for inst in os.listdir(inst_path):
        with open(os.path.join(inst_path, inst), 'r') as f:
            json_data = f.read()
        instance = json.loads(json_data)
    # Открываем каждый файл из папки с JSON-схемами
        for sch in os.listdir(sch_path):
            with open(os.path.join(sch_path, sch), 'r') as s:
                schema_data = s.read()
            schema = json.loads(schema_data)
            # Валидация каждого файла при помощи каждой схемы по очереди
            validator = jsonschema.Draft7Validator(schema)
            # Позволяет вывести все ошибки, а не только первую
            errors = validator.iter_errors(instance)
            # Выводим сообщение об ошибках
            for error in errors:
                print('Ошибка в файле '+inst+', найденная схемой '+sch)
                # Выполняется, если причина ошибки валидации -
                # отсутсвующее свойство в файле
                if error.validator == 'required':
                    print('Нет нужного свойства в файле')
                    print(error.message)
                    print("--------------------------------------------------")
                # Выполняется, если причина ошибки валидации - несоответствие
                # типов данных в схеме и файле
                if error.validator == 'type':
                    print('Тип поля в файле не совпадает в типом поля в схеме')
                    print(error.message)
                    print("--------------------------------------------------")
    # Закрываем файл записи логов скрипта
    sys.stdout.close()


valid('task_folder/event/', 'task_folder/schema/')
