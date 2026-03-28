import dataclasses
import enum
from typing import override

from . import _logic


@dataclasses.dataclass
class auth_ticket_item:
    ticket: str
    user_id: int
    kind: str
    created: int
    expiry: int


class database(_logic.sqlite_connector_base):
    TABLE_NAME = "auth_ticket"

    class field(enum.Enum):
        TICKET = '"ticket"'
        USER_ID = '"user_id"'
        KIND = '"kind"'
        CREATED = '"created"'
        EXPIRY = '"expiry"'

    @override
    def first_time_setup(self) -> None:
        self.sqlite.execute(
            f"""
            CREATE TABLE IF NOT EXISTS "{self.TABLE_NAME}" (
                {self.field.TICKET.value} TEXT PRIMARY KEY NOT NULL,
                {self.field.USER_ID.value} INTEGER NOT NULL,
                {self.field.KIND.value} TEXT NOT NULL,
                {self.field.CREATED.value} INTEGER NOT NULL,
                {self.field.EXPIRY.value} INTEGER NOT NULL
            );
            """,
        )
        self.sqlite.execute(
            f"""
            CREATE INDEX IF NOT EXISTS "idx_{self.TABLE_NAME}_user_id"
            ON "{self.TABLE_NAME}" ({self.field.USER_ID.value});
            """,
        )
        self.sqlite.execute(
            f"""
            CREATE INDEX IF NOT EXISTS "idx_{self.TABLE_NAME}_kind"
            ON "{self.TABLE_NAME}" ({self.field.KIND.value});
            """,
        )

    def update(
        self,
        ticket: str,
        user_id: int,
        kind: str,
        created: int,
        expiry: int,
    ) -> None:
        self.sqlite.execute(
            f"""
            INSERT INTO "{self.TABLE_NAME}"
            (
                {self.field.TICKET.value},
                {self.field.USER_ID.value},
                {self.field.KIND.value},
                {self.field.CREATED.value},
                {self.field.EXPIRY.value}
            )
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT({self.field.TICKET.value})
            DO UPDATE SET
                {self.field.USER_ID.value} = excluded.{self.field.USER_ID.value},
                {self.field.KIND.value} = excluded.{self.field.KIND.value},
                {self.field.CREATED.value} = excluded.{self.field.CREATED.value},
                {self.field.EXPIRY.value} = excluded.{self.field.EXPIRY.value}
            """,
            (
                ticket,
                user_id,
                kind,
                created,
                expiry,
            ),
        )

    def check(
        self,
        ticket: str,
    ) -> tuple[int, str, int, int] | None:
        result = self.sqlite.execute_and_fetch(
            query=f"""
            SELECT
            {self.field.USER_ID.value},
            {self.field.KIND.value},
            {self.field.CREATED.value},
            {self.field.EXPIRY.value}

            FROM "{self.TABLE_NAME}"
            WHERE {self.field.TICKET.value} = ?
            """,
            values=(ticket,),
        )
        row = self.unwrap_result(result)
        if row is None:
            return None
        return (
            int(row[0]),
            str(row[1]),
            int(row[2]),
            int(row[3]),
        )

    def check_object(self, ticket: str) -> auth_ticket_item | None:
        row = self.check(ticket)
        if row is None:
            return None
        return auth_ticket_item(
            ticket=ticket,
            user_id=row[0],
            kind=row[1],
            created=row[2],
            expiry=row[3],
        )

    def delete(self, ticket: str) -> None:
        self.sqlite.execute(
            f"""
            DELETE FROM "{self.TABLE_NAME}"
            WHERE {self.field.TICKET.value} = ?
            """,
            (ticket,),
        )

    def delete_expired(self, current_time: int) -> None:
        self.sqlite.execute(
            f"""
            DELETE FROM "{self.TABLE_NAME}"
            WHERE {self.field.EXPIRY.value} < ?
            """,
            (current_time,),
        )
