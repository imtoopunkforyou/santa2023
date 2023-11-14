import os
import sqlite3
from typing import List, Tuple

from conf import PLAYERS_WITH_WISHES
from utils import make_pairs


class SQLiteClientException(Exception):
    """Exception for SQLiteClient."""

    def __init__(self, message: str = None):
        self.message = '\n' + message if message else None
        super().__init__(self.message)


class SQLiteClient(object):
    def __init__(self, name: str):
        self.name = name + '.db'
        self.path = './' + self.name
        self.connection = sqlite3.connect(self.path, check_same_thread=False)
        self.cursor = self.connection.cursor()

    def _commit(
        self,
        cursor: sqlite3.Cursor,
    ) -> None:
        self.connection.commit()
        cursor.close()

    def initialize(self) -> None:
        query = '''
        CREATE TABLE IF NOT EXISTS players(
            id INTEGER PRIMARY KEY UNIQUE,
            name TEXT NOT NULL,
            wish TEXT DEFAULT NULL,
            santa_id INTEGER DEFAULT NULL UNIQUE,
            telegram_id INTEGER DEFAULT NULL UNIQUE
            );
        '''
        cursor = self.connection.cursor()
        cursor.execute(query)
        self._commit(cursor)

    def drop_db(self) -> None:
        os.remove(self.path)

    def insert_players(self) -> None:
        if len(PLAYERS_WITH_WISHES) % 2 != 0:
            raise SQLiteClientException('The number of players must be even.')

        cursor = self.connection.cursor()

        query = '''SELECT * FROM players;'''
        records = cursor.execute(query).fetchall()
        if records:
            self._commit(cursor)
            return None

        for player_name, player_wish in PLAYERS_WITH_WISHES:
            if player_wish:
                query = '''
                INSERT INTO players (name, wish)
                VALUES ('%s', '%s');
                ''' % (player_name, player_wish)
            else:
                query = '''
                INSERT INTO players (name)
                VALUES ('%s');
                ''' % (player_name)

            cursor.execute(query)
        self._commit(cursor)

    def temp_show_all(self):  # TODO delete.................................................................................
        query = '''
        SELECT * FROM players;
        '''
        cursor = self.connection.cursor()
        a = cursor.execute(query)
        print('*'*30)
        print(a.fetchall())
        print('*'*30)
        self._commit(cursor)

    def appoint_santas(self) -> None:
        cursor = self.connection.cursor()
        cursor.row_factory = lambda cursor, row: row[0]

        player_ids: List[int, ...] = cursor.execute(
            '''SELECT id FROM players;''',
            ).fetchall()
        pairs: List[Tuple[int, int]] = make_pairs(player_ids)

        for player_id, santa_id in pairs:
            query = '''
            UPDATE players SET santa_id = '%s'
            WHERE id = '%s'
            AND santa_id IS NULL;
            ''' % (santa_id, player_id)
            cursor.execute(query)

        self._commit(cursor)

    def get_players(self) -> List[Tuple[int, str]]:
        cursor = self.connection.cursor()
        query = '''
        SELECT id, name FROM players;
        '''
        players = cursor.execute(query).fetchall()
        self._commit(cursor)

        return players

    def get_player_for_santa(
        self,
        santa_id: str,
    ) -> Tuple[str, str]:
        cursor = self.connection.cursor()
        query = '''
        SELECT name, wish
        FROM players
        WHERE santa_id = '%s';
        ''' % (santa_id, )
        player_for_santa = cursor.execute(query).fetchone()
        self._commit(cursor)

        if not player_for_santa:
            raise SQLiteClientException(
                'Player for Santa not found.',
            )

        return player_for_santa

    def insert_telegram_id(
        self,
        player_id: int,
        telegram_id: int,
    ) -> None:
        cursor = self.connection.cursor()
        query = '''
        UPDATE players
        SET telegram_id = '%s'
        WHERE id = '%s';
        ''' % (telegram_id, player_id)
        cursor.execute(query)

        self._commit(cursor)