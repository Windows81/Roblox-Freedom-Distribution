import dataclasses
import enum
from typing import override

from . import _logic


@dataclasses.dataclass
class auth_session_item:
    token: str
    user_id: int
    created: int
    expiry: int
    ip: str


class database(_logic.sqlite_connector_base):
    TABLE_NAME = "auth_session"

    class field(enum.Enum):
        TOKEN = '"token"'
        USER_ID = '"user_id"'
        CREATED = '"created"'
        EXPIRY = '"expiry"'
        IP = '"ip"'

    @override
    def first_time_setup(self) -> None:
        self.sqlite.execute(
            f"""
            CREATE TABLE IF NOT EXISTS "{self.TABLE_NAME}" (
                {self.field.TOKEN.value} TEXT PRIMARY KEY NOT NULL,
                {self.field.USER_ID.value} INTEGER NOT NULL,
                {self.field.CREATED.value} INTEGER NOT NULL,
                {self.field.EXPIRY.value} INTEGER NOT NULL,
                {self.field.IP.value} TEXT NOT NULL
            );
            """,
        )
        self.sqlite.execute(
            f"""
            CREATE INDEX IF NOT EXISTS "idx_{self.TABLE_NAME}_user_id"
            ON "{self.TABLE_NAME}" ({self.field.USER_ID.value});
            """,
        )

    def update(
        self,
        token: str,
        user_id: int,
        created: int,
        expiry: int,
        ip: str,
    ) -> None:
        self.sqlite.execute(
            f"""
            INSERT INTO "{self.TABLE_NAME}"
            (
                {self.field.TOKEN.value},
                {self.field.USER_ID.value},
                {self.field.CREATED.value},
                {self.field.EXPIRY.value},
                {self.field.IP.value}
            )
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT({self.field.TOKEN.value})
            DO UPDATE SET
                {self.field.USER_ID.value} = excluded.{self.field.USER_ID.value},
                {self.field.CREATED.value} = excluded.{self.field.CREATED.value},
                {self.field.EXPIRY.value} = excluded.{self.field.EXPIRY.value},
                {self.field.IP.value} = excluded.{self.field.IP.value}
            """,
            (
                token,
                user_id,
                created,
                expiry,
                ip,
            ),
        )

    def check(
        self,
        token: str,
    ) -> tuple[int, int, int, str] | None:
        result = self.sqlite.execute_and_fetch(
            query=f"""
            SELECT
            {self.field.USER_ID.value},
            {self.field.CREATED.value},
            {self.field.EXPIRY.value},
            {self.field.IP.value}

            FROM "{self.TABLE_NAME}"
            WHERE {self.field.TOKEN.value} = ?
            """,
            values=(token,),
        )
        row = self.unwrap_result(result)
        if row is None:
            return None
        return (
            int(row[0]),
            int(row[1]),
            int(row[2]),
            str(row[3]),
        )

    def check_object(self, token: str) -> auth_session_item | None:
        row = self.check(token)
        if row is None:
            return None
        return auth_session_item(
            token=token,
            user_id=row[0],
            created=row[1],
            expiry=row[2],
            ip=row[3],
        )

    def delete(self, token: str) -> None:
        self.sqlite.execute(
            f"""
            DELETE FROM "{self.TABLE_NAME}"
            WHERE {self.field.TOKEN.value} = ?
            """,
            (token,),
        )

    def delete_expired(self, current_time: int) -> None:
        self.sqlite.execute(
            f"""
            DELETE FROM "{self.TABLE_NAME}"
            WHERE {self.field.EXPIRY.value} < ?
            """,
            (current_time,),
        )
