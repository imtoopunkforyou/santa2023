import csv
from typing import Tuple


def read_players() -> Tuple[Tuple[str, str]]:
    """Read players from csv file at the start of the game."""
    with open('players.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        temp = []
        for row in spamreader:
            if row[1] == 'None':
                row[1] = None
            temp.append(row)

    return tuple((name, wish) for name, wish in temp[1:])
