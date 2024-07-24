from . import _logic
import enum
import json


class database(_logic.sqlite_connector_base):
    TABLE_NAME = "persistence"

    class field(enum.Enum):
        SCOPE = '"scope"'
        TARGET = '"target"'
        KEY = '"key"'
        VALUE = '"value"'

    def first_time_setup(self) -> None:
        self.sqlite.execute(
            f"""
            CREATE TABLE IF NOT EXISTS "{self.TABLE_NAME}" (
                {self.field.SCOPE.value} TEXT NOT NULL,
                {self.field.TARGET.value} TEXT NOT NULL,
                {self.field.KEY.value} TEXT NOT NULL,
                {self.field.VALUE.value} TEXT,
                PRIMARY KEY(
                    {self.field.SCOPE.value},
                    {self.field.TARGET.value},
                    {self.field.KEY.value}
                ) ON CONFLICT REPLACE
            );
            """,
        )
        self.sqlite.commit()

    def set(self, scope: str, target: str, key: str, value) -> None:
        value_str = json.dumps(value)
        self.sqlite.execute(
            f"""
            INSERT INTO "{self.TABLE_NAME}"
            (
                {self.field.SCOPE.value},
                {self.field.TARGET.value},
                {self.field.KEY.value},
                {self.field.VALUE.value}
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                scope,
                target,
                key,
                value_str,
            ),
        )
        self.sqlite.commit()

    def get(self, scope: str, target: str, key: str):
        result: dict | None = self.sqlite.execute(
            f"""
            SELECT
            {self.field.VALUE.value}

            FROM "{self.TABLE_NAME}"
            WHERE {self.field.SCOPE.value} = {repr(scope)}
            AND {self.field.TARGET.value} = {repr(target)}
            AND {self.field.KEY.value} = {repr(key)}
            """,
        ).fetchone()
        if result is None:
            return None

        value = result[0]
        return json.loads(value)
