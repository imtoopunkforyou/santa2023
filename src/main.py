from bot.admin import *
from bot.base import *
from bot.personal import *
from clients import bot, db

if __name__ == '__main__':
    db.initialize()
    db.insert_players()
    db.appoint_santas()

    bot.polling(non_stop=True)
