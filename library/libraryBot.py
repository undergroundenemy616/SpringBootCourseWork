import json
import os

import requests
from dotenv import load_dotenv
from telegram import (Bot, KeyboardButton, ReplyKeyboardMarkup,
                      ReplyKeyboardRemove, Update)
from telegram.ext import (CommandHandler, ConversationHandler, Filters,
                          MessageHandler, Updater)


load_dotenv()

def help_handler(bot: Bot, update: Update):
    update.message.reply_text(
        text=(f'Я твой личный библиотекарь '
              f'.\n\n1. Введи /journal для работы с журналом записей \n\n2. Введи /books для '
              f'работы с книгами.\n\n3. Введи /bookTypes для работы с типами книг.'
              f'\n\n4. Введи /clients для работы с клиентами\n5. Введи /auth для получение токена')
    )

def journal_start_handler(bot: Bot, update: Update):
    reply_markup = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="Посмотреть все записи"), KeyboardButton(text="Посмотреть запись по id"),
                ],
                [
                    KeyboardButton(text="Добавить запись"), KeyboardButton(text="Изменить запись"),
                ],
                [
                    KeyboardButton(text="Удалить запись"),  KeyboardButton(text="Отмена")
                ],
            ],
            resize_keyboard=True
        )
    update.message.reply_text(
        "Что будем делать?",
        reply_markup=reply_markup,
    )
    return "journal_move"


def books_start_handler(bot: Bot, update: Update):
    reply_markup = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="Посмотреть все книги"), KeyboardButton(text="Посмотреть книгу по id"),
                ],
                [
                    KeyboardButton(text="Добавить книгу"), KeyboardButton(text="Изменить книгу"),
                ],
                [
                    KeyboardButton(text="Удалить книгу"),  KeyboardButton(text="Отмена")
                ],
            ],
            resize_keyboard=True
        )
    update.message.reply_text(
        "Что будем делать?",
        reply_markup=reply_markup,
    )
    return "book_move"


def book_types_start_handler(bot: Bot, update: Update):
    reply_markup = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="Посмотреть все типы"), KeyboardButton(text="Посмотреть тип по id"),
                ],
                [
                    KeyboardButton(text="Добавить тип"), KeyboardButton(text="Изменить тип"),
                ],
                [
                    KeyboardButton(text="Удалить тип"),  KeyboardButton(text="Отмена")
                ],
            ],
            resize_keyboard=True
        )
    update.message.reply_text(
        "Что будем делать?",
        reply_markup=reply_markup,
    )
    return "book_types_move"


def clients_start_handler(bot: Bot, update: Update):
    reply_markup = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="Посмотреть всех клиентов"), KeyboardButton(text="Посмотреть клиента по id"),
                ],
                [
                    KeyboardButton(text="Добавить клиента"), KeyboardButton(text="Изменить клиента"),
                ],
                [
                    KeyboardButton(text="Удалить клиента"),  KeyboardButton(text="Отмена")
                ],
            ],
            resize_keyboard=True
        )
    update.message.reply_text(
        "Что будем делать?",
        reply_markup=reply_markup,
    )
    return "clients_move"

def auth_start_handler(bot: Bot, update: Update, user_data: dict):
    update.message.reply_text(
        text="Прикрепите JSON файл с username и password",
        reply_markup=ReplyKeyboardRemove(),
    )
    return "auth2"

def auth2_start_handler(bot: Bot, update: Update, user_data: dict):
    journ = update.message.text
    try:
        journ_json = json.loads(journ)
    except Exception as e:
        update.message.reply_text(
            text="Неправильный JSON файл",
            reply_markup=ReplyKeyboardRemove(),
        )
        return ConversationHandler.END
    journal = requests.post('http://localhost:8181/libr/singin', json=journ_json)
    if journal.status_code == 400 or journal.status_code == 500 or journal.status_code == 403:
        update.message.reply_text(
            text=f"Ошибка парсинга  JSON-файла -{journal.json()['message']}",
            reply_markup=ReplyKeyboardRemove(),
        )
    else:
        update.message.reply_text(
            text=f"Ваш токен: {journal.json()['token']}",
            reply_markup=ReplyKeyboardRemove(),
        )
    return ConversationHandler.END


def journal_move_handler(bot: Bot, update: Update, user_data: dict):
    if update.message.text == "Посмотреть все записи":
        journal = requests.get('http://localhost:8181/libr/journals').json()
        for jour in journal:
            update.message.reply_text(
                text=f"ID записи: {jour['id']}\nНазвание книги: {jour['book']['name']}\nИмя клиента: {jour['client']['firstName']}"
                     f"\nДень взятия: {jour['dateBegin']}"
                     f"\nДедлайн сдачи {jour['dateEnd']}\nДень возврата {jour['dateReturn']}",
                reply_markup=ReplyKeyboardRemove(),
            )
        return ConversationHandler.END
    elif update.message.text == "Посмотреть запись по id":
        update.message.reply_text(
            text="Введите ID записи",
            reply_markup=ReplyKeyboardRemove(),
        )
        return "journal_find_id"
    elif update.message.text == "Добавить запись":
        user_data['method'] = "journal_post"
        update.message.reply_text(
            text="Введите JWT токен",
            reply_markup=ReplyKeyboardRemove(),
        )
        return "jwt"
    elif update.message.text == "Изменить запись":
        user_data['method'] = "journal_put"
        update.message.reply_text(
            text="Введите JWT токен",
            reply_markup=ReplyKeyboardRemove(),
        )
        return "jwt"
    elif update.message.text == "Удалить запись":
        user_data['method'] = "journal_delete"
        update.message.reply_text(
            text="Введите JWT токен",
            reply_markup=ReplyKeyboardRemove(),
        )
        return "jwt"
    elif update.message.text == "Отмена":
        update.message.reply_text(
            text="Ок",
            reply_markup=ReplyKeyboardRemove(),
        )
        return ConversationHandler.END
    else:
        update.message.reply_text(
            text="Я вас не понял",
        )
        return ConversationHandler.entry_points


def book_move_handler(bot: Bot, update: Update, user_data: dict):
    if update.message.text == "Посмотреть все книги":
        journal = requests.get('http://localhost:8181/libr/books').json()
        for jour in journal:
            update.message.reply_text(
                text=f"ID книги: {jour['id']}\nНазвание книги: {jour['name']}\nКоличество: {jour['cnt']}"
                     f"\nТип книги: {jour['bookType']['name']}",
                reply_markup=ReplyKeyboardRemove(),
            )
        return ConversationHandler.END
    elif update.message.text == "Посмотреть книгу по id":
        update.message.reply_text(
            text="Введите ID книги",
            reply_markup=ReplyKeyboardRemove(),
        )
        return "book_find_id"
    elif update.message.text == "Добавить книгу":
        user_data['method'] = "book_post"
        update.message.reply_text(
            text="Введите JWT токен",
            reply_markup=ReplyKeyboardRemove(),
        )
        return "jwt"
    elif update.message.text == "Изменить книгу":
        user_data['method'] = "book_put"
        update.message.reply_text(
            text="Введите JWT токен",
            reply_markup=ReplyKeyboardRemove(),
        )
        return "jwt"
    elif update.message.text == "Удалить книгу":
        user_data['method'] = "book_delete"
        update.message.reply_text(
            text="Введите JWT токен",
            reply_markup=ReplyKeyboardRemove(),
        )
        return "jwt"
    elif update.message.text == "Отмена":
        update.message.reply_text(
            text="Ок",
            reply_markup=ReplyKeyboardRemove(),
        )
        return ConversationHandler.END
    else:
        update.message.reply_text(
            text="Я вас не понял",
        )
        return ConversationHandler.entry_points


def book_types_move_handler(bot: Bot, update: Update, user_data: dict):
    if update.message.text == "Посмотреть все типы":
        journal = requests.get('http://localhost:8181/libr/bookTypes').json()
        for jour in journal:
            update.message.reply_text(
                text=f"ID типа: {jour['id']}\nНазвание типа: {jour['name']}\nШтраф: {jour['fine']}"
                     f"\nКоличество дней {jour['dayCount']}",
                reply_markup=ReplyKeyboardRemove(),
            )
        return ConversationHandler.END
    elif update.message.text == "Посмотреть тип по id":
        update.message.reply_text(
            text="Введите ID типа",
            reply_markup=ReplyKeyboardRemove(),
        )
        return "book_types_find_id"
    elif update.message.text == "Добавить тип":
        user_data['method'] = "book_types_post"
        update.message.reply_text(
            text="Введите JWT токен",
            reply_markup=ReplyKeyboardRemove(),
        )
        return "jwt"
    elif update.message.text == "Изменить тип":
        user_data['method'] = "book_types_put"
        update.message.reply_text(
            text="Введите JWT токен",
            reply_markup=ReplyKeyboardRemove(),
        )
        return "jwt"
    elif update.message.text == "Удалить тип":
        user_data['method'] = "book_types_delete"
        update.message.reply_text(
            text="Введите JWT токен",
            reply_markup=ReplyKeyboardRemove(),
        )
        return "jwt"
    elif update.message.text == "Отмена":
        update.message.reply_text(
            text="Ок",
            reply_markup=ReplyKeyboardRemove(),
        )
        return ConversationHandler.END
    else:
        update.message.reply_text(
            text="Я вас не понял",
        )
        return ConversationHandler.entry_points


def clients_move_handler(bot: Bot, update: Update, user_data: dict):
    if update.message.text == "Посмотреть всех клиентов":
        journal = requests.get('http://localhost:8181/libr/clients').json()
        for jour in journal:
            update.message.reply_text(
                text=f"ID клиента: {jour['id']}\nИмя: {jour['firstName']} {jour['lastName']} {jour['fatherName']}"
                     f"\nСерия паспорта {jour['passportSeria']} \nНомер паспорта {jour['passportNum']}",
                reply_markup=ReplyKeyboardRemove(),
            )
        return ConversationHandler.END
    elif update.message.text == "Посмотреть клиента по id":
        update.message.reply_text(
            text="Введите ID клиента",
            reply_markup=ReplyKeyboardRemove(),
        )
        return "clients_find_id"
    elif update.message.text == "Добавить клиента":
        user_data['method'] = "clients_post"
        update.message.reply_text(
            text="Введите JWT токен",
            reply_markup=ReplyKeyboardRemove(),
        )
        return "jwt"
    elif update.message.text == "Изменить клиента":
        user_data['method'] = "clients_put"
        update.message.reply_text(
            text="Введите JWT токен",
            reply_markup=ReplyKeyboardRemove(),
        )
        return "jwt"
    elif update.message.text == "Удалить клиента":
        user_data['method'] = "clients_delete"
        update.message.reply_text(
            text="Введите JWT токен",
            reply_markup=ReplyKeyboardRemove(),
        )
        return "jwt"
    elif update.message.text == "Отмена":
        update.message.reply_text(
            text="Ок",
            reply_markup=ReplyKeyboardRemove(),
        )
        return ConversationHandler.END
    else:
        update.message.reply_text(
            text="Я вас не понял",
        )
        return ConversationHandler.entry_points


def journal_find_id_handler(bot: Bot, update: Update, user_data: dict):
    id = update.message.text
    journ = requests.get(f'http://localhost:8181/libr/journal/{id}')
    if journ.status_code == 404:
        update.message.reply_text(
            text="Записи с таким ID не найдено",
            reply_markup=ReplyKeyboardRemove(),
        )
    else:
        jour = journ.json()
        update.message.reply_text(
            text=f"ID записи: {jour['id']}\nНазвание книги: {jour['book']['name']}\nИмя клиента: {jour['client']['firstName']}"
                 f" \nДень взятия: {jour['dateBegin']}"
                 f"\nДедлайн сдачи {jour['dateEnd']}\nДень возврата {jour['dateReturn']}",
            reply_markup=ReplyKeyboardRemove(),
        )
    return ConversationHandler.END


def book_find_id_handler(bot: Bot, update: Update, user_data: dict):
    id = update.message.text
    journ = requests.get(f'http://localhost:8181/libr/book/{id}')
    if journ.status_code == 404:
        update.message.reply_text(
            text="Книги с таким ID не найдено",
            reply_markup=ReplyKeyboardRemove(),
        )
    else:
        jour = journ.json()
        update.message.reply_text(
            text=f"ID книги: {jour['id']}\nНазвание книги: {jour['name']}\nКоличество: {jour['cnt']}"
                 f"\nТип книги {jour['bookType']['name']}",
            reply_markup=ReplyKeyboardRemove(),
        )
    return ConversationHandler.END


def book_types_find_id_handler(bot: Bot, update: Update, user_data: dict):
    id = update.message.text
    journ = requests.get(f'http://localhost:8181/libr/bookTypes/{id}')
    if journ.status_code == 404:
        update.message.reply_text(
            text="Типа с таким ID не найдено",
            reply_markup=ReplyKeyboardRemove(),
        )
    else:
        jour = journ.json()
        update.message.reply_text(
            text=f"ID типа: {jour['id']}\nНазвание типа: {jour['name']}\nШтраф: {jour['fine']}"
                 f"\nКоличество дней {jour['dayCount']}",
            reply_markup=ReplyKeyboardRemove(),
        )
    return ConversationHandler.END


def clients_find_id_handler(bot: Bot, update: Update, user_data: dict):
    id = update.message.text
    journ = requests.get(f'http://localhost:8181/libr/client/{id}')
    if journ.status_code == 404:
        update.message.reply_text(
            text="Клиента с таким ID не найдено",
            reply_markup=ReplyKeyboardRemove(),
        )
    else:
        jour = journ.json()
        update.message.reply_text(
            text=f"ID клиента: {jour['id']}\nИмя: {jour['firstName']} {jour['lastName']} {jour['fatherName']}"
                 f"\nСерия паспорта {jour['passportSeria']} \nНомер паспорта {jour['passportNum']}",
            reply_markup=ReplyKeyboardRemove(),
        )
    return ConversationHandler.END


def journal_post_handler(bot: Bot, update: Update, user_data: dict):
    journ = update.message.text
    try:
        journ_json = json.loads(journ)
    except Exception as e:
        update.message.reply_text(
            text="Неправильный JSON файл",
            reply_markup=ReplyKeyboardRemove(),
        )
        return ConversationHandler.END
    journal = requests.post('http://localhost:8181/libr/addJournal', json=journ_json,
                            headers={f'Authorization': user_data['tok']})
    if journal.status_code == 400 or journal.status_code == 500:
        update.message.reply_text(
            text=f"Ошибка парсинга  JSON-файла -{journal.json()['message']}",
            reply_markup=ReplyKeyboardRemove(),
        )
    else:
        update.message.reply_text(
            text="Журнал добавлен",
            reply_markup=ReplyKeyboardRemove(),
        )
    return ConversationHandler.END


def book_post_handler(bot: Bot, update: Update, user_data: dict):
    journ = update.message.text
    try:
        journ_json = json.loads(journ)
    except Exception as e:
        update.message.reply_text(
            text="Неправильный JSON файл",
            reply_markup=ReplyKeyboardRemove(),
        )
        return ConversationHandler.END
    journal = requests.post('http://localhost:8181/libr/addBook', json=journ_json, headers={f'Authorization': user_data['tok']})
    if journal.status_code == 400 or journal.status_code == 500:
        update.message.reply_text(
            text=f"Ошибка парсинга  JSON-файла -{journal.json()['message']}",
            reply_markup=ReplyKeyboardRemove(),
        )
    else:
        update.message.reply_text(
        text="Книга добавлена",
        reply_markup=ReplyKeyboardRemove(),
    )
    return ConversationHandler.END


def book_types_post_handler(bot: Bot, update: Update, user_data: dict):
    journ = update.message.text
    try:
        journ_json = json.loads(journ)
    except Exception as e:
        update.message.reply_text(
            text="Неправильный JSON файл",
            reply_markup=ReplyKeyboardRemove(),
        )
        return ConversationHandler.END
    journal = requests.post('http://localhost:8181/libr/addBookType', json=journ_json,
                            headers={f'Authorization': user_data['tok']})
    if journal.status_code == 400 or journal.status_code == 500:
        update.message.reply_text(
            text=f"Ошибка парсинга  JSON-файла -{journal.json()['message']}",
            reply_markup=ReplyKeyboardRemove(),
        )
    else:
        update.message.reply_text(
            text="Тип добавлен",
            reply_markup=ReplyKeyboardRemove(),
        )
    return ConversationHandler.END


def clients_post_handler(bot: Bot, update: Update, user_data: dict):
    print("FUKCIT")
    journ = update.message.text
    try:
        journ_json = json.loads(journ)
    except Exception as e:
        update.message.reply_text(
            text="Неправильный JSON файл",
            reply_markup=ReplyKeyboardRemove(),
        )
        return ConversationHandler.END
    journal = requests.post('http://localhost:8181/libr/addClient', json=journ_json,
                            headers={f'Authorization': user_data['tok']})
    print(journal.status_code)
    if journal.status_code == 400 or journal.status_code == 500:
        update.message.reply_text(
            text=f"Ошибка парсинга  JSON-файла -{journal.json()['message']}",
            reply_markup=ReplyKeyboardRemove(),
        )
    elif journal.status_code == 200:
        update.message.reply_text(
            text="Клиент добавлен",
            reply_markup=ReplyKeyboardRemove(),
        )
    return ConversationHandler.END


def journal_put_handler(bot: Bot, update: Update, user_data: dict):
    user_data['id'] = update.message.text
    journ = requests.get(f'http://localhost:8181/libr/journal/{user_data["id"]}')
    if journ.status_code == 404 or journ.status_code == 500:
        update.message.reply_text(
            text="Записи с таким ID не найдено",
            reply_markup=ReplyKeyboardRemove(),
        )
    else:
        update.message.reply_text(
            text="Отправьте JSON файл записи",
            reply_markup=ReplyKeyboardRemove(),
        )
        return "journal_put_2"


def book_put_handler(bot: Bot, update: Update, user_data: dict):
    user_data['id'] = update.message.text
    journ = requests.get(f'http://localhost:8181/libr/book/{user_data["id"]}')
    if journ.status_code == 404:
        update.message.reply_text(
            text="Книги с таким ID не найдено",
            reply_markup=ReplyKeyboardRemove(),
        )
    else:
        update.message.reply_text(
            text="Отправьте JSON файл книги",
            reply_markup=ReplyKeyboardRemove(),
        )
        return "book_put_2"


def book_types_put_handler(bot: Bot, update: Update, user_data: dict):
    user_data['id'] = update.message.text
    journ = requests.get(f'http://localhost:8181/libr/bookType/{user_data["id"]}')
    if journ.status_code == 404:
        update.message.reply_text(
            text="Типа с таким ID не найдено",
            reply_markup=ReplyKeyboardRemove(),
        )
    else:
        update.message.reply_text(
            text="Отправьте JSON файл типа",
            reply_markup=ReplyKeyboardRemove(),
        )
        return "book_types_put_2"


def clients_put_handler(bot: Bot, update: Update, user_data: dict):
    user_data['id'] = update.message.text
    journ = requests.get(f'http://localhost:8181/libr/client/{user_data["id"]}')
    if journ.status_code == 404:
        update.message.reply_text(
            text="Клиента с таким ID не найдено",
            reply_markup=ReplyKeyboardRemove(),
        )
    else:
        update.message.reply_text(
            text="Отправьте JSON файл типа",
            reply_markup=ReplyKeyboardRemove(),
        )
        return "clients_put_2"


def journal_put_handler2(bot: Bot, update: Update, user_data: dict):
    journ = update.message.text
    try:
        journ_json = json.loads(journ)
    except Exception as e:
        update.message.reply_text(
            text="Неправильный JSON файл",
            reply_markup=ReplyKeyboardRemove(),
        )
        return ConversationHandler.END
    journal = requests.put(f'http://localhost:8181/libr/editJournal/{user_data["id"]}', json=journ_json, headers={f'Authorization': user_data['tok']})
    if journal.status_code == 500:
        update.message.reply_text(
            text=f"Ошибка - {journal['message']}",
            reply_markup=ReplyKeyboardRemove(),
        )
    else:
        update.message.reply_text(
            text="Запись обновлена",
            reply_markup=ReplyKeyboardRemove(),
        )
    return ConversationHandler.END


def book_put_handler2(bot: Bot, update: Update, user_data: dict):
    journ = update.message.text
    try:
        journ_json = json.loads(journ)
    except Exception as e:
        update.message.reply_text(
            text="Неправильный JSON файл",
            reply_markup=ReplyKeyboardRemove(),
        )
        return ConversationHandler.END
    journal = requests.put(f'http://localhost:8181/libr/editBook/{user_data["id"]}', json=journ_json, headers={f'Authorization': user_data['tok']})
    if journal.status_code == 500:
        update.message.reply_text(
            text=f"Ошибка - {journal['message']}",
            reply_markup=ReplyKeyboardRemove(),
        )
    else:
        update.message.reply_text(
            text="Книга обновлена",
            reply_markup=ReplyKeyboardRemove(),
        )
    return ConversationHandler.END


def book_types_put_handler2(bot: Bot, update: Update, user_data: dict):
    journ = update.message.text
    try:
        journ_json = json.loads(journ)
    except Exception as e:
        update.message.reply_text(
            text="Неправильный JSON файл",
            reply_markup=ReplyKeyboardRemove(),
        )
        return ConversationHandler.END
    journal = requests.put(f'http://localhost:8181/libr/editBookType/{user_data["id"]}', json=journ_json, headers={f'Authorization': user_data['tok']})
    if journal.status_code == 500:
        update.message.reply_text(
            text=f"Ошибка - {journal['message']}",
            reply_markup=ReplyKeyboardRemove(),
        )
    else:
        update.message.reply_text(
            text="Тип обновлена",
            reply_markup=ReplyKeyboardRemove(),
        )
    return ConversationHandler.END


def clients_put_handler2(bot: Bot, update: Update, user_data: dict):
    journ = update.message.text
    try:
        journ_json = json.loads(journ)
    except Exception as e:
        update.message.reply_text(
            text="Неправильный JSON файл",
            reply_markup=ReplyKeyboardRemove(),
        )
        return ConversationHandler.END
    journal = requests.put(f'http://localhost:8181/libr/editClient/{user_data["id"]}', json=journ_json, headers={f'Authorization': user_data['tok']})
    if journal.status_code == 500:
        update.message.reply_text(
            text=f"Ошибка - {journal['message']}",
            reply_markup=ReplyKeyboardRemove(),
        )
    else:
        update.message.reply_text(
            text="Клиент обновлен",
            reply_markup=ReplyKeyboardRemove(),
        )
    return ConversationHandler.END


def journal_delete_handler(bot: Bot, update: Update, user_data: dict):
    user_data['id'] = update.message.text
    journ = requests.get(f'http://localhost:8181/libr/edtJournal/{user_data["id"]}')
    if journ.status_code == 404:
        update.message.reply_text(
            text="Записи с таким ID не найдено",
            reply_markup=ReplyKeyboardRemove(),
        )
    else:
        journal = requests.delete(f'http://localhost:8181/libr/deleteJournal{user_data["id"]}', headers={f'Authorization': user_data['tok']})
        update.message.reply_text(
            text="Запись удалена",
            reply_markup=ReplyKeyboardRemove(),
        )
    return ConversationHandler.END


def book_delete_handler(bot: Bot, update: Update, user_data: dict):
    user_data['id'] = update.message.text
    journ = requests.get(f'http://localhost:8181/libr/book/{user_data["id"]}')
    print(journ.status_code)
    if journ.status_code == 404:
        update.message.reply_text(
            text="Книги с таким ID не найдено",
            reply_markup=ReplyKeyboardRemove(),
        )
    else:
        journal = requests.delete(f'http://localhost:8181/libr/deleteBook/{user_data["id"]}', headers={f'Authorization': user_data['tok']})
        update.message.reply_text(
            text="Книга удалена",
            reply_markup=ReplyKeyboardRemove(),
        )
    return ConversationHandler.END


def book_types_delete_handler(bot: Bot, update: Update, user_data: dict):
    user_data['id'] = update.message.text
    journ = requests.get(f'http://localhost:8181/libr/bookType/{user_data["id"]}')
    if journ.status_code == 404:
        update.message.reply_text(
            text="Типа с таким ID не найдено",
            reply_markup=ReplyKeyboardRemove(),
        )
    else:
        journal = requests.delete(f'http://localhost:8181/libr/deleteBookType/{user_data["id"]}', headers={f'Authorization': user_data['tok']})
        update.message.reply_text(
            text="Тип удален",
            reply_markup=ReplyKeyboardRemove(),
        )
    return ConversationHandler.END


def clients_delete_handler(bot: Bot, update: Update, user_data: dict):
    user_data['id'] = update.message.text
    journ = requests.get(f'http://localhost:8181/libr/client/{user_data["id"]}')
    if journ.status_code == 404:
        update.message.reply_text(
            text="Клиента с таким ID не найдено",
            reply_markup=ReplyKeyboardRemove(),
        )
    else:
        journal = requests.delete(f'http://localhost:8181/libr/deleteClient/{user_data["id"]}', headers={f'Authorization': user_data['tok']})
        update.message.reply_text(
            text="Клиент удален",
            reply_markup=ReplyKeyboardRemove(),
        )
    return ConversationHandler.END



def jwt_handler(bot: Bot, update: Update, user_data: dict):
    jwt = update.message.text
    user_data['tok'] = "Bearer " + jwt
    journ = requests.post(f'http://localhost:8181/libr/journals', headers={f'Authorization': user_data['tok']})
    if journ.status_code == 403 or journ.status_code == 500:
        update.message.reply_text(
            text="Неправильный токен или доступ запрещен",
            reply_markup=ReplyKeyboardRemove(),
        )
        return ConversationHandler.END
    else:
        if user_data['method'] == "journal_post" or user_data['method'] == "book_post" or user_data['method'] == "book_types_post" or user_data['method'] == "clients_post":
            update.message.reply_text(
                text="Прикрепите JSON файл объекта",
                reply_markup=ReplyKeyboardRemove(),
            )
        else:
            update.message.reply_text(
                text="Напишите ID объекта",
                reply_markup=ReplyKeyboardRemove(),
            )
        return user_data['method']

def main():
    bot = Bot(
        token=os.getenv('TELEGRAM_TOKEN')
    )
    updater = Updater(
        bot=bot
    )
    print(updater.bot.get_me())
    conv_handler = ConversationHandler(allow_reentry=True,
        entry_points=[
            CommandHandler('journal', journal_start_handler),
            CommandHandler('books', books_start_handler),
            CommandHandler('book_types', book_types_start_handler),
            CommandHandler('clients', clients_start_handler),
            CommandHandler('auth', auth_start_handler, pass_user_data=True),


        ],
        states={
            "journal_move": [
                MessageHandler(Filters.text, journal_move_handler, pass_user_data=True),
            ],
            "auth2": [
                MessageHandler(Filters.text, auth2_start_handler, pass_user_data=True),
            ],
            "journal_find_id": [
                MessageHandler(Filters.text, journal_find_id_handler, pass_user_data=True),
            ],
            "journal_post": [
                MessageHandler(Filters.text, journal_post_handler, pass_user_data=True),
            ],
            "journal_put": [
                MessageHandler(Filters.text, journal_put_handler, pass_user_data=True),
            ],
            "journal_put_2": [
                MessageHandler(Filters.text, journal_put_handler2, pass_user_data=True),
            ],
            "journal_delete": [
                MessageHandler(Filters.text, journal_delete_handler, pass_user_data=True),
            ],
            "book_move": [
                MessageHandler(Filters.text, book_move_handler, pass_user_data=True),
            ],
            "book_find_id": [
                MessageHandler(Filters.text, book_find_id_handler, pass_user_data=True),
            ],
            "book_post": [
                MessageHandler(Filters.text, book_post_handler, pass_user_data=True),
            ],
            "book_put": [
                MessageHandler(Filters.text, book_put_handler, pass_user_data=True),
            ],
            "book_put_2": [
                MessageHandler(Filters.text, book_put_handler2, pass_user_data=True),
            ],
            "book_delete": [
                MessageHandler(Filters.text, book_delete_handler, pass_user_data=True),
            ],
            "book_types_move": [
                MessageHandler(Filters.text, book_types_move_handler, pass_user_data=True),
            ],
            "book_types_find_id": [
                MessageHandler(Filters.text, book_types_find_id_handler, pass_user_data=True),
            ],
            "book_types_post": [
                MessageHandler(Filters.text, book_types_post_handler, pass_user_data=True),
            ],
            "book_types_put": [
                MessageHandler(Filters.text, book_types_put_handler, pass_user_data=True),
            ],
            "book_types_put_2": [
                MessageHandler(Filters.text, book_types_put_handler2, pass_user_data=True),
            ],
            "book_types_delete": [
                MessageHandler(Filters.text, book_types_delete_handler, pass_user_data=True),
            ],
            "clients_move": [
                MessageHandler(Filters.text, clients_move_handler, pass_user_data=True),
            ],
            "clients_find_id": [
                MessageHandler(Filters.text, clients_find_id_handler, pass_user_data=True),
            ],
            "clients_post": [
                MessageHandler(Filters.text, clients_post_handler, pass_user_data=True),
            ],
            "clients_put": [
                MessageHandler(Filters.text, clients_put_handler, pass_user_data=True),
            ],
            "clients_put_2": [
                MessageHandler(Filters.text, clients_put_handler2, pass_user_data=True),
            ],
            "clients_delete": [
                MessageHandler(Filters.text, clients_delete_handler, pass_user_data=True),
            ],
            "jwt": [
                MessageHandler(Filters.text, jwt_handler, pass_user_data=True),
            ],

        },
        fallbacks=[
        ],
    )

    updater.dispatcher.add_handler(conv_handler)
    updater.dispatcher.add_handler(CommandHandler('help', help_handler))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
