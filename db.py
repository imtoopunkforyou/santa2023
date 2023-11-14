import os
import sqlite3
from typing import List, Tuple, Union, Optional

from conf import PLAYERS_WITH_WISHES
from utils import make_pairs
import time


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
    
    def select_all(
        self,
    ) -> List[Tuple[int, str, Union[str, None], Union[int, None], Union[int, None]]]:
        cursor = self.connection.cursor()
        query = '''
        SELECT * FROM players;
        '''
        players = cursor.execute(query).fetchall()
        self._commit(cursor)
        
        return players


    
    def insert_wish(
        self,
        wish: str,
        player_telegram_id: int,
    ) -> None:
        cursor = self.connection.cursor()
        query = '''
        UPDATE players
        SET wish = '%s'
        WHERE telegram_id = '%s';
        ''' % (wish, player_telegram_id)
        cursor.execute(query)
        self._commit(cursor)

    def get_player_info(
        self,
        player_telegram_id: int,
    ) -> Tuple[str, str, str]:
        cursor = self.connection.cursor()
        gift_for_query = '''
        SELECT name, wish FROM players
        WHERE santa_id =
        (SELECT id FROM players
        WHERE telegram_id = '%s');
        ''' % (player_telegram_id, )
        gift_for: str = cursor.execute(gift_for_query).fetchone()[0]
        wish_for: str = cursor.execute(gift_for_query).fetchone()[1]
        query = '''
        SELECT name, wish FROM players
        WHERE telegram_id = '%s'
        ''' % (player_telegram_id, )
        name, wish = cursor.execute(query).fetchone()
        self._commit(cursor)

        return name, wish, wish_for, gift_for
    
    def cheque_telegram_id(
        self,
        player_telegram_id: int,
    ) -> bool:
        cursor = self.connection.cursor()
        query = '''
        SELECT * FROM players
        WHERE telegram_id = '%s';
        ''' % (player_telegram_id)
        result = cursor.execute(query).fetchone()
        self._commit(cursor)

        if result:
            return True

        return False

    def add_two_players(
        self,
        names: Tuple[str, str],
    ):  # TODO create only one query
        cursor = self.connection.cursor()
        
        last_id_query = '''
        SELECT id FROM players
        ORDER BY id DESC
        LIMIT 1;
        '''
        last_id = cursor.execute(last_id_query).fetchone()[0]
        
        first_player_id = last_id + 1
        second_player_id = last_id + 2
        
        query_first_player = '''
        INSERT INTO players (id, name, santa_id)
        VALUES ('%s', '%s', '%s');
        ''' % (first_player_id, names[0], second_player_id)

        query_second_player = '''
        INSERT INTO players (id, name, santa_id)
        VALUES ('%s', '%s', '%s');
        ''' % (second_player_id, names[1], first_player_id)

        cursor.execute(query_first_player)
        cursor.execute(query_second_player)

        self._commit(cursor)
    
    def delete_telegram_id(
        self,
        name: str,
    ):
        cursor = self.connection.cursor()
        query = '''
        UPDATE players
        SET telegram_id = NULL
        WHERE name = '%s';
        ''' % (name, )
        cursor.execute(query)

        self._commit(cursor)

