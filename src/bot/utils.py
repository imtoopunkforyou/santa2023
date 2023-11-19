from typing import Callable, Union

from telebot import TeleBot
from telebot.types import Message

import conf


def is_admin(func: Callable) -> Union[Callable, None]:
    """Use a decorator to check user permissions."""
    def _is_admin(message: Message):
        if message.chat.id in conf.BOT_ADMINS:
            return func(message)

        return

    return _is_admin


def ban_slash_in_message(bot: TeleBot) -> Union[Callable, None]:
    """Use a decorator to check slash in message."""
    def wrapper(func: Callable):
        def _cheque_slash_in_message(message: Message):
            if '/' in message.text:
                bot.send_message(
                    message.chat.id,
                    'Упс, что-то пошло не так :(',
                )
                return

            return func(message)

        return _cheque_slash_in_message

    return wrapper
