from sqlite3 import IntegrityError

from db import SQLiteClientException
from enums import CommandsEnum
from clients import db, bot
from utils import is_admin
from telebot.types import Message


# =============
# Base commands
# =============


@bot.message_handler(commands=[CommandsEnum.START.value])
def start(message: Message) -> None:
    bot.send_message(
        message.chat.id,
        'Привет! Я бот, который создаёт пары для тайного санты!\n'
        f'Напиши мне /{CommandsEnum.LIST.value}',
    )


@bot.message_handler(commands=[CommandsEnum.HELP.value])
def show_help(message: Message) -> None:
    msg = ''
    for i in tuple('/' + i for i in CommandsEnum.get_values()):
        msg += i + '\n'

    bot.send_message(
        message.chat.id,
        'Доступные комманды:\n' + msg,
    )


@bot.message_handler(commands=[CommandsEnum.LIST.value])
def show_players(message: Message) -> None:
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


# ===================
# Individual commands
# ===================


@bot.message_handler(commands=[CommandsEnum.ME.value])
def show_info(message: Message) -> None:
    telegram_id = message.chat.id
    if not db.cheque_telegram_id(telegram_id):
        bot.send_message(
            telegram_id,
            f'Сначала нужно выбрать себя в списке: /{CommandsEnum.LIST.value}',
        )
        return

    name, wish, wish_for, gift_for = db.get_player_info(telegram_id)
    bot.send_message(
        telegram_id,
        f'Имя: {name}\n'
        f'Твоё желание: {wish}\n'
        f'Даришь подарок для: {gift_for}\n'
        f'Он(а) желает: {wish_for if wish_for else "не указано"}',
    )


@bot.message_handler(commands=[CommandsEnum.WISH.value])
def input_wish(message: Message) -> None:
    telegram_id = message.chat.id
    if not db.cheque_telegram_id(telegram_id):
        bot.send_message(
            telegram_id,
            f'Сначала нужно выбрать себя в списке: /{CommandsEnum.LIST.value}',
        )
        return

    response = bot.send_message(message.chat.id, 'Напиши своё пожелание!')
    bot.register_next_step_handler(response, insert_wish)

def insert_wish(message: Message) -> None:
    telegram_id = message.chat.id
    db.insert_wish(
        wish=message.text,
        player_telegram_id=telegram_id,
        )
    bot.send_message(
        telegram_id,
        'Я добавил твоё пожелание!',
    )


# ===================
# For admins commands
# ===================


@bot.message_handler(commands=[CommandsEnum.DB.value])
def show_db(message: Message) -> None:
    telegram_id = message.chat.id

    if not is_admin(telegram_id):
        bot.send_message(
            telegram_id,
            'Жулик! Ты не админ!',
        )
        return

    players = db.select_all()
    for player in players:
        player_id = player[0]
        player_name = player[1]
        player_wish = player[2]
        player_santa_id = player[3]
        player_telegram_id = player[4]

        bot.send_message(
            telegram_id,
            f'Игрок {player_name}:\n'
            f'ID в базе данных: {player_id}\n'
            f'Пожелание: {player_wish}\n'
            f'Санта игрока: {player_santa_id}\n'
            f'ID игрока в телеграмме (если есть, значит уже участвует): {player_telegram_id}',
        )
    bot.send_message(
        telegram_id,
        f'Всего игроков: {len(players)}',
    )


@bot.message_handler(commands=[CommandsEnum.ADD_PLAYERS.value])
def insert_players(message: Message) -> None:
    telegram_id = message.chat.id

    if not is_admin(telegram_id):
        bot.send_message(
            telegram_id,
            'Жулик! Ты не админ!',
        )
        return

    response = bot.send_message(
        telegram_id,
        'Напиши имена двух игроков в виде:\n'
        'Генадий Букин, Дарья Букина\n\n'
        'Они станут сантами друг для друга!\n'
        'Пожалания они смогут добавить позже самостоятельно :)',
        )
    bot.register_next_step_handler(response, add_players)


def add_players(message: Message) -> None:
    telegram_id = message.chat.id
    player_names = tuple(message.text.split(', '))
    if len(player_names) != 2:
        bot.send_message(
            telegram_id,
            'Упс, что-то пошло не так, но ничего не сломалось!\n'
            f'Попробуй ещё раз: /{CommandsEnum.ADD_PLAYERS.value}',
        )
        return
    db.add_two_players(player_names)
    bot.send_message(
        telegram_id,
        f'Добавил ребят в список: /{CommandsEnum.LIST.value}',
    )


@bot.message_handler(commands=[CommandsEnum.RESTORE_PLAYER.value])
def restore_player(message: Message) -> None:
    telegram_id = message.chat.id

    if not is_admin(telegram_id):
        bot.send_message(
            telegram_id,
            'Жулик! Ты не админ!',
        )
        return

    response = bot.send_message(
        telegram_id,
        f'Напиши имя игрока так же, как он записан в /{CommandsEnum.LIST.value}\n'
        'Я прерву его регистрацию и он сможет заново зарегистрироваться\n\n'
        'Это безопасная штука и сделана для того случая, когда кто-то неправильно введёт цифру из списка',
        )
    bot.register_next_step_handler(response, restore_telegram_id)


def restore_telegram_id(message: Message) -> None:
    db.delete_telegram_id(message.text)
    bot.send_message(
        message.chat.id,
        'Готово! :)',
    )


if __name__ == '__main__':
    db.initialize()
    db.insert_players()
    db.appoint_santas()

    bot.polling(non_stop=True)
