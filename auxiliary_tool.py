import requests
from requests.exceptions import HTTPError
import json
import logging

LOG1 = logging.getLogger(__name__)
# logging.basicConfig(format="%(name)s %(asctime)s %(levelname)s %(message)s",
#                     datefmt='%d-%b-%y %H:%M:%S',
#                     level=logging.INFO,
#                     filename="py_log.log",
#                     filemode="w"
#                     )


def write_file(file: str, data: str) -> None:
    """
    Сохраняем строковые данные в указанный файл.
    :param file: путь к файлу
    :param data: сохраняемые данные
    :return: None
    """
    with open(file, 'w', encoding="utf-8") as f:
        f.write(data)


def read_file(file: str) -> str:
    """
    Читаем файл и возвращаем прочитанные данные.
    :param file: путь к файлу
    :return: прочитанные данные
    """
    with open(file, 'r', encoding="utf-8") as f:
        return f.read()


def get_response(url: str, cookies: dict, headers: dict) -> str:
    """
    Отправляем запрос по указаному url. Если статус ответа получаем 200, то отдаем html текст страницы.
    Иначе обрабатываем исключения, выдавая пустую строку.
    :param url: путь для HTTP запроса.
    :param headers: HTTP заголовок запроса.
    :return: текст HTML страницы или пустую строку в случае исключения.
    """
    try:
        response = requests.get(url, cookies=cookies, headers=headers)
        response.raise_for_status()
        return response.text
    except HTTPError as http_err:
        LOG1.error(f"Ошибка HTTP: {http_err}")
        return ""
    except Exception as err:
        LOG1.error(f"Произошла другая ошибка: {err}")
        return ""


def save_json(file: str, to_json: dict) -> None:
    """
    Сохраняем полученные данные в формате JSON
    :param file: путь к файлу для сохранения.
    :param to_json: Любой словарь для записи.
    :return: None
    """
    with open(file, 'w', encoding="utf-8") as f:
        json.dump(to_json, f, indent=4, ensure_ascii=False, separators=(',', ': '))
        LOG1.info(f"Список записан в файл {file}.")


def load_json(file_name: str) -> dict:
    """
    Десериализация JSON файла.
    При ошибке чтения файла, вернёт пустой список, чтобы последующий цикл не отработал.
    :param file_name: путь к json файлу.
    :return: dict
    """
    try:
        with open(file_name, "r", encoding="utf-8") as f:
            LOG1.info(f"Файл {file_name} успешно прочитан.")
            return json.load(f)
    except Exception as e:
        LOG1.error(f" Файл {file_name} или директория отсутствуют. \n {e}")
        return {}


if __name__ == '__main__':
    print("auxiliary_tool.py")
