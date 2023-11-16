import csv
import os
from typing import Tuple


def read_players_from_csv() -> Tuple[Tuple[str, str]]:
    """Read players from csv file at the start of the game."""
    with open('players.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        temp = []
        for row in spamreader:
            if row[1] == 'None':
                row[1] = None
            temp.append(row)

    return tuple((name, wish) for name, wish in temp[1:])


BOT_TOKEN = os.getenv('BOT_TOKEN')
PLAYERS_WITH_WISHES = read_players_from_csv()
BOT_ADMINS = tuple(os.getenv('BOT_ADMINS').split(','))
DATABASE_NAME = os.getenv('DATABASE_NAME')
