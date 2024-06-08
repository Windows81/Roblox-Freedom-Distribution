import enum
import sqlite3
import os.path

PLAYER_TABLE_NAME = "players"


class player_field(enum.Enum):
    USER_CODE = "user_code"
    USERNAME = "username"
    ID_NUMBER = "id_number"


class storager:
    def __init__(self, path: str) -> None:
        self.first_time = not os.path.isfile(path)
        self.sqlite = sqlite3.connect(path)
        if self.first_time:
            self.first_time_setup()

    def first_time_setup(self):
        self.sqlite.execute(
            f"""
            CREATE TABLE "{PLAYER_TABLE_NAME}" (
                "{player_field.USER_CODE.value}" TEXT NOT NULL UNIQUE,
                "{player_field.USERNAME.value}" TEXT NOT NULL UNIQUE,
                "{player_field.ID_NUMBER.value}" INTEGER NOT NULL UNIQUE,
                PRIMARY KEY("USER_CODE")
            );
            """,
        )
        self.sqlite.commit()

    def get_player_field_from_index(self, index: player_field, value: int | str | None, field: player_field):
        if index == player_field.ID_NUMBER:
            value = self.sanitise_id_num(value)

        if not value:
            return None

        result: dict | None = self.sqlite.execute(
            f"""
            SELECT FROM "{PLAYER_TABLE_NAME}" WHERE ? = ?
            """,
            (index, repr(value)),
        ).fetchone()
        if not result:
            return None
        return result[field]

    def sanitise_id_num(self, id_num: str | int | None) -> int | None:
        if not id_num:
            return None
        return int(id_num)
