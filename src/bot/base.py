from sqlite3 import IntegrityError

from telebot.types import KeyboardButton, Message, ReplyKeyboardMarkup

from clients import bot, db
from db.db import SQLiteClientException

from .enums import CommandsEnum


@bot.message_handler(commands=[CommandsEnum.BASE_START.value])
def start(message: Message) -> None:
    """
    First step command.

    Args:
        message (Message): telegram message from telegram user.
    """
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    for command in CommandsEnum.get_user_commands():
        button = KeyboardButton(command)
        markup.add(button)

    bot.send_message(
        message.chat.id,
        'Привет!\nЯ бот, который создаёт пары для тайного Санты.\n'
        f'🎅🏻 Для регистрации напиши /{CommandsEnum.BASE_LIST.value} и отправь мне свой номер из списка участников.\n'
        f'🎁 Для того, чтобы рассказать твоему Тайному Санте о своих пожеланиях, напиши /{CommandsEnum.PERSONAL_WISH.value}.'
        f'⛄ Для того, чтобы я напомнил тебе всю информацию о твоем подопечном напиши /{CommandsEnum.PERSONAL_ME.value}. Рекомендую обязательно сделать это через пару дней: возможно, за это время он придумает и добавит свое пожелание.))'
        f'❓ Список всех команд можно увидеть, если напишешь /{CommandsEnum.BASE_HELP.value}.',
        reply_markup=markup,
    )


@bot.message_handler(commands=[CommandsEnum.BASE_HELP.value])
def show_help(message: Message) -> None:
    """
    Show all commands.

    Args:
        message (Message): telegram message from telegram user.
    """

    start(message)

    #bot.send_message(
    #    message.chat.id,
    #    'Привет! Я бот, который создаёт пары для тайного Санты!\n'
    #    f'Для регистрации напиши мне /{CommandsEnum.BASE_LIST.value} и отправь мне свой номер из списка участников.\n'
    #    'А еще ты можешь написать пожелание для своего тайного Санты, чтобы ему было проще выбрать подарок для тебя! '
    #    f'Сделать это можно с помощью команды /{CommandsEnum.PERSONAL_WISH.value}\n'
    #    f'Если хочешь, чтобы я напомнил всю информацию о твоем подопечном - просто напиши мне /{CommandsEnum.PERSONAL_ME.value}\n'
    #    f'Список всех доступных команд можно увидеть, если напишешь /{CommandsEnum.BASE_HELP.value}',
    #)


@bot.message_handler(commands=[CommandsEnum.BASE_LIST.value])
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


@bot.message_handler(regexp=r'^([1-9][0-9]?|100)$')  # numbers 1-100
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
        f'Пожелание твоего подопечного: {player_wish if player_wish else "не указано"}',
    )
