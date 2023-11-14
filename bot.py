from sqlite3 import IntegrityError

import telebot
from telebot import types

from conf import BOT_TOKEN, DATABASE_NAME
from db import SQLiteClient, SQLiteClientException

db = SQLiteClient(DATABASE_NAME)

bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(
        types.KeyboardButton('/list'),
    )

    bot.send_message(
        message.chat.id,
        'Привет! Я бот, который создаёт пары для тайного санты! Напиши мне /list',
        reply_markup=markup,
    )


@bot.message_handler(commands=['list'])
def show_players(message):
    players = db.get_players()
    title = 'Выбери своё имя!\nПожалуйста, пришли мне только номер :)\n\n\n'
    msg = 'Номер участника | Имя \n\n'+'\n'.join(['. '.join(map(str, i)) for i in players])

    bot.send_message(
        message.chat.id,
        title + msg,
    )


@bot.message_handler(regexp=r'^([1-9][0-9]?|100)$')  # numbers 1-100  TODO добавить инлайн подтвержение
def input_santa_id(message):
    santa_id: int = int(message.text)
    santa_telegram_id: int = message.chat.id

    try:
        db.insert_telegram_id(
            santa_id,
            santa_telegram_id,
        )
    except IntegrityError:
        msg = 'Вы уже являетесь тайным сантой.'
        bot.send_message(
            santa_telegram_id,
            msg,
        )
        return

    try:
        player_name, player_wish = db.get_player_for_santa(santa_id)
    except SQLiteClientException:
        msg = 'Упс, что-то пошло не так :('
        bot.send_message(
            santa_telegram_id,
            msg,
        )
        return

    bot.send_message(
        santa_telegram_id,
        'Ты большой молодец! '
        f'Ты стал(а) Тайным Сантой для {player_name}.\n'
        f'Пожалание игрока: {player_wish if player_wish else "не указано"}',
    )


if __name__ == '__main__':
    db.initialize()
    db.insert_players()
    db.appoint_santas()
    db.get_players()

    bot.polling(non_stop=True)
