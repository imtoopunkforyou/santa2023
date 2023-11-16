import os

from utils import read_players

BOT_TOKEN = os.getenv('BOT_TOKEN')
PLAYERS_WITH_WISHES = read_players()
BOT_ADMINS = tuple(int(i) for i in os.getenv('BOT_ADMINS').split(','))
DATABASE_NAME = os.getenv('DATABASE_NAME')
