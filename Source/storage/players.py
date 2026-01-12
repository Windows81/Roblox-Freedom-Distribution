from typing import override
from . import _logic
import enum


class database(_logic.sqlite_connector_base):
    TABLE_NAME = "players"

    class player_field(enum.Enum):
        USERCODE = '"user_code"'
        IDEN_NUM = '"id_number"'
        USERNAME = '"username"'

    @override
    def first_time_setup(self) -> None:
        self.sqlite.execute(
            f"""
            CREATE TABLE IF NOT EXISTS "{self.TABLE_NAME}" (
                {self.player_field.USERCODE.value} TEXT NOT NULL,
                {self.player_field.IDEN_NUM.value} INTEGER NOT NULL,
                {self.player_field.USERNAME.value} TEXT NOT NULL,
                PRIMARY KEY(
                    {self.player_field.USERCODE.value}
                ) ON CONFLICT IGNORE,
                UNIQUE ({self.player_field.USERCODE.value}) ON CONFLICT IGNORE,
                UNIQUE ({self.player_field.IDEN_NUM.value}) ON CONFLICT IGNORE,
                UNIQUE ({self.player_field.USERNAME.value}) ON CONFLICT IGNORE
            );
            """,
        )

    def add_player(self, usercode: str, iden_num: int, username: str) -> tuple[int, str] | None:
        '''
        Adds a new player to the database and returns the first entry which corresponds with the newly-added player.
        If a player already exists, return the player's iden number and username, which may be different from what gets provided as arguments.

        Tries to get the entry whose user code matches, else fail.

        Returns a tuple with the following:
        `int`: corresponds with the iden number of a user with that user code in the database.
        `str`: corresponds with the username of a user with that user code in the database.
        '''
        self.sqlite.execute(
            f"""
            INSERT INTO "{self.TABLE_NAME}"
            (
                {self.player_field.USERCODE.value},
                {self.player_field.IDEN_NUM.value},
                {self.player_field.USERNAME.value}
            )
            VALUES (?, ?, ?)
            """,
            (
                usercode,
                iden_num,
                username,
            ),
        )
        return self.check(usercode)

    def get_player_field_from_index(
        self,
        index: player_field,
        value: int | str | None,
        field: player_field,
    ):
        if index == self.player_field.IDEN_NUM:
            value = self.sanitise_player_iden_num(value)

        if value is None:
            return None

        result = self.sqlite.execute_and_fetch(
            f"""
            SELECT {field.value} FROM "{self.TABLE_NAME}" WHERE {index.value} = ?
            """,
            (value,),
        )
        return self.unwrap_result(result)

    def check(self, usercode: str) -> tuple[int, str] | None:
        '''
        Checks if a player with a particular field value exists.

        Returns a tuple with the following:
        `int`: corresponds with the iden number of a user whose `index` field matches `value`.
        `str`: corresponds with the username of a user whose `index` field matches `value`.
        '''
        result = self.sqlite.execute_and_fetch(
            f"""
            SELECT
            {self.player_field.IDEN_NUM.value},
            {self.player_field.USERNAME.value}

            FROM "{self.TABLE_NAME}" WHERE {self.player_field.USERCODE.value} = ?
            """,
            (usercode,),
        )
        return self.unwrap_result(result)

    def sanitise_player_iden_num(self, iden_num: int | str | None) -> int | None:
        if iden_num is None:
            return None
        return int(iden_num)
