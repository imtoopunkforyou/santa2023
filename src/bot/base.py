from sqlite3 import IntegrityError

from telebot.types import Message

from clients import bot, db
from db.db import SQLiteClientException
from enums import CommandsEnum


@bot.message_handler(commands=[CommandsEnum.START.value])
def start(message: Message) -> None:
    """
    First step command.

    Args:
        message (Message): telegram message from telegram user.
    """
    bot.send_message(
        message.chat.id,
        'Привет! Я бот, который создаёт пары для тайного санты!\n'
        f'Напиши мне /{CommandsEnum.LIST.value}',
    )


@bot.message_handler(commands=[CommandsEnum.HELP.value])
def show_help(message: Message) -> None:
    """
    Show all commands.

    Args:
        message (Message): telegram message from telegram user.
    """
    msg = ''
    for i in tuple('/' + i for i in CommandsEnum.get_values()):
        msg += i + '\n'

    bot.send_message(
        message.chat.id,
        'Доступные комманды:\n' + msg,
    )


@bot.message_handler(commands=[CommandsEnum.LIST.value])
def show_players(message: Message) -> None:
    """
    Show players list.

    Args:
        message (Message): telegram message from telegram user.
    """
    players = db.get_players()

    title = 'Выбери своё имя!\n'
    'Пожалуйста, пришли мне только номер :)\n\n\n'
    msg = 'Номер участника | Имя \n\n'+'\n'.join(['. '.join(map(str, i)) for i in players])

    bot.send_message(
        message.chat.id,
        title + msg,
    )


@bot.message_handler(regexp=CommandsEnum.REGEXP_1_100.value)
def input_santa_id(message: Message) -> None:
    """
    Show Santa who needs a gift.

    Args:
        message (Message): telegram message from telegram user
    """
    santa_id: int = int(message.text)
    santa_telegram_id: int = message.chat.id

    try:
        db.insert_telegram_id(
            santa_id,
            santa_telegram_id,
        )
    except IntegrityError:
        bot.send_message(
            santa_telegram_id,
            'Вы уже являетесь тайным сантой!',
        )
        return

    try:
        player_name, player_wish = db.get_player_for_santa(santa_id)
    except SQLiteClientException:
        bot.send_message(
            santa_telegram_id,
            'Упс, что-то пошло не так :(',
        )
        return

    bot.send_message(
        santa_telegram_id,
        'Ты большой молодец!\n'
        f'Ты стал(а) Тайным Сантой для {player_name}.\n'
        f'Пожалание игрока: {player_wish if player_wish else "не указано"}',
    )
