from . import _logic
import enum


class database(_logic.sqlite_connector_base):
    TABLE_NAME = "players"

    class player_field(enum.Enum):
        USER_CODE = '"user_code"'
        ID_NUMBER = '"id_number"'
        USERNAME = '"username"'

    def first_time_setup(self) -> None:
        self.sqlite.execute(
            f"""
            CREATE TABLE IF NOT EXISTS "{self.TABLE_NAME}" (
                {self.player_field.USER_CODE.value} TEXT NOT NULL,
                {self.player_field.ID_NUMBER.value} INTEGER NOT NULL,
                {self.player_field.USERNAME.value} TEXT NOT NULL,
                PRIMARY KEY(
                    {self.player_field.USER_CODE.value}
                ) ON CONFLICT IGNORE,
                UNIQUE ({self.player_field.USER_CODE.value}) ON CONFLICT IGNORE,
                UNIQUE ({self.player_field.ID_NUMBER.value}) ON CONFLICT IGNORE,
                UNIQUE ({self.player_field.USERNAME.value}) ON CONFLICT IGNORE
            );
            """,
        )
        self.sqlite.commit()

    def add_player(self, user_code: str, id_num: int, username: str) -> tuple[str, int, str]:
        self.sqlite.execute(
            f"""
            INSERT INTO "{self.TABLE_NAME}"
            (
                {self.player_field.USER_CODE.value},
                {self.player_field.ID_NUMBER.value},
                {self.player_field.USERNAME.value}
            )
            VALUES (?, ?, ?)
            """,
            (
                user_code,
                id_num,
                username,
            ),
        )
        self.sqlite.commit()
        result = self.sqlite.execute(
            f"""
            SELECT
            {self.player_field.USER_CODE.value},
            {self.player_field.ID_NUMBER.value},
            {self.player_field.USERNAME.value}

            FROM "{self.TABLE_NAME}"
            WHERE {self.player_field.USER_CODE.value} = {repr(user_code)}
            """,
        ).fetchone()
        return result

    def get_player_field_from_index(self, index: player_field, value, field: player_field):
        if index == self.player_field.ID_NUMBER:
            value = self.sanitise_player_id_num(value)

        if value is None:
            return None

        result = self.sqlite.execute(
            f"""
            SELECT {field.value} FROM "{self.TABLE_NAME}" WHERE {index.value} = {repr(value)}
            """,
        ).fetchone()
        if result is None:
            return None
        return result[0]

    def check(self, index: player_field, value) -> bool:
        '''
        Checks if a player with a particular field value exists.
        '''
        if index == self.player_field.ID_NUMBER:
            value = self.sanitise_player_id_num(value)

        if value is None:
            return False

        result = self.sqlite.execute(
            f"""
            SELECT * FROM "{self.TABLE_NAME}" WHERE {index.value} = {repr(value)}
            """,
        ).fetchone()
        return result is not None

    def sanitise_player_id_num(self, id_num: str | int | None) -> int | None:
        if id_num is None:
            return None
        return int(id_num)
