from telebot.types import Message

from clients import bot, db

from .enums import CommandsEnum
from .utils import ban_slash_in_message


@bot.message_handler(commands=[CommandsEnum.PERSONAL_ME.value])
def show_info(message: Message) -> None:
    """
    Player info for player.

    Args:
        message (Message): telegram message from telegram user.
    """
    telegram_id = message.chat.id
    if not db.cheque_telegram_id(telegram_id):
        bot.send_message(
            telegram_id,
            f'Сначала нужно выбрать себя в списке: /{CommandsEnum.BASE_LIST.value}',
        )
        return

    name, wish, wish_for, gift_for = db.get_player_info(telegram_id)
    bot.send_message(
        telegram_id,
        f'Имя: {name}\n'
        f'Твоё желание: {wish}\n'
        f'Даришь подарок для: {gift_for}\n'
        f'Твой подопечный желает: {wish_for if wish_for else "не указано"}',
    )


@bot.message_handler(commands=[CommandsEnum.PERSONAL_WISH.value])
def input_wish(message: Message) -> None:
    """
    Add wish for player.

    Args:
        message (Message): telegram message from telegram user.
    """
    telegram_id = message.chat.id
    if not db.cheque_telegram_id(telegram_id):
        bot.send_message(
            telegram_id,
            f'Сначала нужно выбрать себя в списке: /{CommandsEnum.BASE_LIST.value}',
        )
        return

    response = bot.send_message(message.chat.id, 'Напиши своё пожелание! Старое пожелание будет заменено на новое.\n'
                                'Пожалуйста, рассчитывай, что подарки мы дарим в пределах 1000 рублей')
    bot.register_next_step_handler(response, insert_wish)


@ban_slash_in_message(bot)
def insert_wish(message: Message) -> None:
    """Next step handler for input_wish(...)."""
    telegram_id = message.chat.id

    db.insert_wish(
        wish=message.text,
        player_telegram_id=telegram_id,
        )
    bot.send_message(
        telegram_id,
        'Я обновил твоё пожелание!',
    )
