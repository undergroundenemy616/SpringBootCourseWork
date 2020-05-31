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
        text=(f'Я умею одновременно публиковать посты в группы социальных сетей, а конкретно в  и '
              f'.\n\n1. Введи /journal для работы с журналом записей \n\n2. Введи /books для '
              f'работы с книгами.\n\n3. Введи /bookTypes для работы с типами книг.'
              f'\n\n4. Введи /clients для работы с клиентами')
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


def journal_move_handler(bot: Bot, update: Update, user_data: dict):
    if update.message.text == "Посмотреть все записи":
        journal = requests.get('http://localhost:8181/libr/journals').json()
        for jour in journal:
            update.message.reply_text(
                text=f"ID записи: {jour['id']}\nНазвание книги: {jour['book']['name']}\nИмя клиента: {jour['client']['firstName']}"
                     f" {jour['client']['firstName']}\nДень взятия: {jour['dateBegin']}"
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
        update.message.reply_text(
            text="Отправьте JSON файл записи",
            reply_markup=ReplyKeyboardRemove(),
        )
        return "journal_post"
    elif update.message.text == "Изменить запись":
        update.message.reply_text(
            text="Введите ID записи",
            reply_markup=ReplyKeyboardRemove(),
        )
        return "journal_put"
    elif update.message.text == "Удалить запись":
        update.message.reply_text(
            text="Введите ID записи",
            reply_markup=ReplyKeyboardRemove(),
        )
        return "journal_delete"
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
                     f"\nТип книги {jour['bookType']}",
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
        update.message.reply_text(
            text="Отправьте JSON файл книги",
            reply_markup=ReplyKeyboardRemove(),
        )
        return "book_post"
    elif update.message.text == "Изменить книгу":
        update.message.reply_text(
            text="Введите ID книги",
            reply_markup=ReplyKeyboardRemove(),
        )
        return "book_put"
    elif update.message.text == "Удалить книгу":
        update.message.reply_text(
            text="Введите ID книги",
            reply_markup=ReplyKeyboardRemove(),
        )
        return "book_delete"
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
        print(jour['book']['name'])
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
                 f"\nТип книги {jour['bookType']}",
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
    journal = requests.post('http://localhost:8181/libr/addJournal', json=journ_json)
    update.message.reply_text(
        text="Запись добавлена",
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
    journal = requests.post('http://localhost:8181/libr/addBook', json=journ_json)
    update.message.reply_text(
        text="Книга добавлена",
        reply_markup=ReplyKeyboardRemove(),
    )
    return ConversationHandler.END


def journal_put_handler(bot: Bot, update: Update, user_data: dict):
    user_data['id'] = update.message.text
    journ = requests.get(f'http://localhost:8181/libr/journal/{user_data["id"]}')
    if journ.status_code == 404:
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
    journal = requests.put(f'http://localhost:8181/libr/editJournal/{user_data["id"]}', json=journ_json)
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
    journal = requests.put(f'http://localhost:8181/libr/editBook/{user_data["id"]}', json=journ_json)
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


def journal_delete_handler(bot: Bot, update: Update, user_data: dict):
    user_data['id'] = update.message.text
    journ = requests.get(f'http://localhost:8181/libr/edtJournal/{user_data["id"]}')
    if journ.status_code == 404:
        update.message.reply_text(
            text="Записи с таким ID не найдено",
            reply_markup=ReplyKeyboardRemove(),
        )
    else:
        journal = requests.delete(f'http://localhost:8181/libr/deleteJournal{user_data["id"]}')
        update.message.reply_text(
            text="Запись удалена",
            reply_markup=ReplyKeyboardRemove(),
        )
    return ConversationHandler.END


def book_delete_handler(bot: Bot, update: Update, user_data: dict):
    user_data['id'] = update.message.text
    journ = requests.get(f'http://localhost:8181/libr/book/{user_data["id"]}')
    if journ.status_code == 404:
        update.message.reply_text(
            text="Книги с таким ID не найдено",
            reply_markup=ReplyKeyboardRemove(),
        )
    else:
        journal = requests.delete(f'http://localhost:8181/libr/deleteBook/{user_data["id"]}')
        update.message.reply_text(
            text="Книга удалена",
            reply_markup=ReplyKeyboardRemove(),
        )
    return ConversationHandler.END


def main():
    bot = Bot(
        token=os.getenv('TELEGRAM_TOKEN')
    )
    updater = Updater(
        bot=bot
    )
    print(updater.bot.get_me())
    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler('journal', journal_start_handler),
            CommandHandler('books', books_start_handler),
            CommandHandler('book_types', book_types_start_handler),
            #CommandHandler('clients', clients_start_handler),

        ],
        states={
            "journal_move": [
                MessageHandler(Filters.text, journal_move_handler, pass_user_data=True),
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
