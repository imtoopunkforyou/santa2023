from telebot.types import Message

from clients import bot, db
from enums import CommandsEnum
from utils import is_admin


@bot.message_handler(commands=[CommandsEnum.DB.value])
def show_db(message: Message) -> None:
    """
    Show info about all players.

    Args:
        message (Message): telegram message.
    """
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
    """
    Add two players to players table.

    Args:
        message (Message): telegram message.
    """
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
    """Next step handler for insert_players(...)."""
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
    """
    Delete player registration (update player telegram id to null).

    Args:
        message (Message): telegram message.
    """
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
    """Next step handler for restore_player(...)."""
    db.delete_telegram_id(message.text)
    bot.send_message(
        message.chat.id,
        'Готово! :)',
    )
