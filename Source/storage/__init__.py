import enum
import queue
import sqlite3
import os.path

PLAYER_TABLE_NAME = "players"


class player_field(enum.Enum):
    USER_CODE = "user_code"
    USERNAME = "username"
    ID_NUMBER = "id_number"


class storager:
    def __init__(self, path: str, force_init: bool) -> None:
        self.first_time = not os.path.isfile(path)
        self.sqlite = sqlite3.connect(path, check_same_thread=False)
        if self.first_time or force_init:
            self.first_time_setup()

    def first_time_setup(self):
        self.sqlite.execute(
            f"""
            DROP TABLE IF EXISTS "{PLAYER_TABLE_NAME}"
            """,
        )
        self.sqlite.execute(
            f"""
            CREATE TABLE "{PLAYER_TABLE_NAME}" (
                {repr(player_field.USER_CODE.value)} TEXT NOT NULL UNIQUE,
                {repr(player_field.USERNAME.value)} TEXT NOT NULL,
                {repr(player_field.ID_NUMBER.value)} INTEGER NOT NULL UNIQUE,
                PRIMARY KEY("USER_CODE")
            );
            """,
        )
        self.sqlite.commit()

    def add_player(self, user_code: str, username: str, id_num: int):
        self.sqlite.execute(
            f"""
            INSERT INTO "{PLAYER_TABLE_NAME}"
            (
                {repr(player_field.USER_CODE.value)},
                {repr(player_field.USERNAME.value)},
                {repr(player_field.ID_NUMBER.value)}
            )
            VALUES
            (
                {repr(user_code)},
                {repr(username)},
                {repr(id_num)}
            )
            ON CONFLICT DO NOTHING
            """,
        )
        self.sqlite.commit()

    def get_player_field_from_index(self, index: player_field, value: int | str | None, field: player_field):
        if index == player_field.ID_NUMBER:
            value = self.sanitise_id_num(value)

        if not value:
            return None

        cur = self.sqlite.cursor()
        result: dict | None = cur.execute(
            f"""
            SELECT ("{field.value}") FROM "{PLAYER_TABLE_NAME}" WHERE {index.value} = {repr(value)}
            """,
        ).fetchone()
        if not result:
            return None
        return result[0]

    def sanitise_id_num(self, id_num: str | int | None) -> int | None:
        if not id_num:
            return None
        return int(id_num)
