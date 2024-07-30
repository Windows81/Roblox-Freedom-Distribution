from . import _logic
import enum


class database(_logic.sqlite_connector_base):
    TABLE_NAME = "funds"

    class field(enum.Enum):
        USER_ID_NUM = '"user_id_num"'
        FUNDS = '"funds"'

    def first_time_setup(self) -> None:
        self.sqlite.execute(
            f"""
            CREATE TABLE IF NOT EXISTS "{self.TABLE_NAME}" (
                {self.field.USER_ID_NUM.value} INTEGER NOT NULL,
                {self.field.FUNDS.value} INTEGER NOT NULL,
                PRIMARY KEY(
                    {self.field.USER_ID_NUM.value}
                ) ON CONFLICT IGNORE
            );
            """,
        )
        self.sqlite.commit()

    def add(self, user_id_num: int, delta: int) -> None:
        self.sqlite.execute(
            f"""
            UPDATE "{self.TABLE_NAME}"
            SET {self.field.FUNDS.value} = {self.field.FUNDS.value} + {delta}
            WHERE {self.field.USER_ID_NUM.value} = {user_id_num}
            """
        )
        self.sqlite.commit()

    def init(self, user_id_num: int, value: int) -> None:
        self.sqlite.execute(
            f"""
            INSERT INTO "{self.TABLE_NAME}"
            VALUES (?, ?)
            """,
            (
                user_id_num,
                value,
            ),
        )
        self.sqlite.commit()

    def set(self, user_id_num: int, value: int) -> None:
        self.sqlite.execute(
            f"""
            UPDATE "{self.TABLE_NAME}"
            SET {self.field.FUNDS.value} = {value}
            WHERE {self.field.USER_ID_NUM.value} = {user_id_num}
            """
        )
        self.sqlite.commit()

    def check(self, user_id_num: int) -> int | None:
        result: dict | None = self.sqlite.execute(
            f"""
            SELECT
            {self.field.FUNDS.value}

            FROM "{self.TABLE_NAME}"
            WHERE {self.field.USER_ID_NUM.value} = {user_id_num}
            """,
        ).fetchone()
        if result is None:
            return None

        return result[0]
