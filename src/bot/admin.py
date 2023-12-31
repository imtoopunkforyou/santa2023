from telebot.types import Message

from clients import bot, db

from .enums import CommandsEnum
from .utils import ban_slash_in_message, is_admin


@bot.message_handler(commands=[CommandsEnum.ADMIN_DB.value])
@is_admin
def show_db(message: Message) -> None:
    """
    Show info about all players.

    Args:
        message (Message): telegram message.
    """
    telegram_id = message.chat.id

    players = db.select_all()
    for player in players:
        player_id = player[0]
        player_name = player[1]
        player_wish = player[2]
        player_santa_name = player[3]
        gift_for = player[4]
        gift_wish = player[5]
        player_telegram_id = player[6]

        bot.send_message(
            telegram_id,
            f'Игрок {player_name}:\n\n'
            f'ID в базе данных: {player_id}\n'
            f'Пожелание игрока: {player_wish}\n'
            f'Санта игрока: {player_santa_name}\n'
            f'Игрок дарит подарок для: {gift_for}\n'
            f'Пожалание того, кому игрок дарит подарок: '
            f'{gift_wish if gift_wish else "Не указано"}\n'
            'ID пользователя в телеграмме: '
            f'{player_telegram_id if player_telegram_id else "игрок ещё не зарегистрировался"}',
        )

    bot.send_message(
        telegram_id,
        f'Всего игроков: {len(players)}',
    )


@bot.message_handler(commands=[CommandsEnum.ADMIN_ADD_PLAYERS.value])
@is_admin
def insert_players(message: Message) -> None:
    """
    Add two players to players table.

    Args:
        message (Message): telegram message.
    """
    telegram_id = message.chat.id

    response = bot.send_message(
        telegram_id,
        'Напиши имена двух игроков в виде:\n'
        'Генадий Букин, Дарья Букина\n\n'
        'Они станут сантами друг для друга!\n'
        'Пожалания они смогут добавить позже самостоятельно :)',
        )
    bot.register_next_step_handler(response, add_players)


@ban_slash_in_message(bot)
def add_players(message: Message) -> None:
    """Next step handler for insert_players(...)."""
    telegram_id = message.chat.id

    player_names = tuple(message.text.split(', '))
    if len(player_names) != 2:
        bot.send_message(
            telegram_id,
            'Упс, что-то пошло не так, но ничего не сломалось!\n'
            f'Попробуй ещё раз: /{CommandsEnum.ADMIN_ADD_PLAYERS.value}',
        )
        return
    db.add_two_players(player_names)
    bot.send_message(
        telegram_id,
        f'Добавил ребят в список: /{CommandsEnum.BASE_LIST.value}',
    )


@bot.message_handler(commands=[CommandsEnum.ADMIN_RESTORE_PLAYER.value])
@is_admin
def restore_player(message: Message) -> None:
    """
    Delete player registration (update player telegram id to null).

    Args:
        message (Message): telegram message.
    """
    telegram_id = message.chat.id

    response = bot.send_message(
        telegram_id,
        f'Напиши имя игрока так же, как он записан в /{CommandsEnum.BASE_LIST.value}\n'
        'Я прерву его регистрацию и он сможет заново зарегистрироваться\n\n'
        'Это безопасная штука и сделана для того случая, когда кто-то неправильно введёт цифру из списка',
        )
    bot.register_next_step_handler(response, restore_telegram_id)


@ban_slash_in_message(bot)
def restore_telegram_id(message: Message) -> None:
    """Next step handler for restore_player(...)."""
    db.delete_telegram_id(message.text)
    bot.send_message(
        message.chat.id,
        'Готово! :)',
    )
