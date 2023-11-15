from telebot import TeleBot

from conf import BOT_TOKEN, DATABASE_NAME
from db import SQLiteClient

db = SQLiteClient(
    name=DATABASE_NAME,
)
bot = TeleBot(
    token=BOT_TOKEN,
)
