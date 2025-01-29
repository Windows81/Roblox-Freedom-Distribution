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

    def add_player(self, user_code: str, id_num: int,
                   username: str) -> tuple[str, int, str] | None:
        '''
        Adds a new player to the database and returns the first entry which corresponds with the newly-added player.
        Tries to get the entry whose username matches, else fail.
        '''
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
        result = self.sqlite.fetch_results(self.sqlite.execute(
            f"""
            SELECT
            {self.player_field.USER_CODE.value},
            {self.player_field.ID_NUMBER.value},
            {self.player_field.USERNAME.value}

            FROM "{self.TABLE_NAME}"
            WHERE
            {self.player_field.USER_CODE.value} = {repr(user_code)}
            """,
        ))
        assert result is not None
        if len(result) > 0:
            return result[0]
        return None

    def get_player_field_from_index(
            self,
            index: player_field,
            value,
            field: player_field):
        if index == self.player_field.ID_NUMBER:
            value = self.sanitise_player_id_num(value)

        if value is None:
            return None

        result = self.sqlite.fetch_results(self.sqlite.execute(
            f"""
            SELECT {field.value} FROM "{self.TABLE_NAME}" WHERE {index.value} = {repr(value)}
            """,
        ))
        assert result is not None
        if len(result) > 0:
            return result[0]
        return None

    def check(self, index: player_field, value) -> bool:
        '''
        Checks if a player with a particular field value exists.
        '''
        if index == self.player_field.ID_NUMBER:
            value = self.sanitise_player_id_num(value)

        if value is None:
            return False

        result = self.sqlite.fetch_results(self.sqlite.execute(
            f"""
            SELECT * FROM "{self.TABLE_NAME}" WHERE {index.value} = {repr(value)}
            """,
        ))
        return result is not None

    def sanitise_player_id_num(self, id_num: int | str | None) -> int | None:
        if id_num is None:
            return None
        return int(id_num)
