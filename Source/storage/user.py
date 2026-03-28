import dataclasses
from datetime import datetime
from typing import override
import enum

from . import _logic


@dataclasses.dataclass
class user_item:
    id: int
    username: str
    password: str
    created: str
    description: str
    lastonline: str
    accountstatus: int
    TOTPEnabled: bool


class database(_logic.sqlite_connector_base):
    TABLE_NAME = "user"

    class field(enum.Enum):
        ID = '"id"'
        USERNAME = '"username"'
        PASSWORD = '"password"'
        CREATED = '"created"'
        DESCRIPTION = '"description"'
        LASTONLINE = '"lastonline"'
        ACCOUNTSTATUS = '"accountstatus"'
        TOTP_ENABLED = '"TOTPEnabled"'

    @override
    def first_time_setup(self) -> None:
        self.sqlite.execute(
            f"""
            CREATE TABLE IF NOT EXISTS "{self.TABLE_NAME}" (
                {self.field.ID.value} INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                {self.field.USERNAME.value} TEXT NOT NULL,
                {self.field.PASSWORD.value} TEXT NOT NULL,
                {self.field.CREATED.value} DATETIME NOT NULL,
                {self.field.DESCRIPTION.value} TEXT NOT NULL DEFAULT 'Hi! I just joined Roblox!',
                {self.field.LASTONLINE.value} DATETIME NOT NULL,
                {self.field.ACCOUNTSTATUS.value} INTEGER NOT NULL DEFAULT 1,
                {self.field.TOTP_ENABLED.value} BOOLEAN NOT NULL DEFAULT FALSE,
                UNIQUE ({self.field.USERNAME.value}) ON CONFLICT ABORT
            );
            """,
        )

    @staticmethod
    def _normalise_timestamp(value: datetime | str | None) -> str:
        if value is None:
            return datetime.utcnow().isoformat()
        if isinstance(value, datetime):
            return value.isoformat()
        return value

    def update(
        self,
        username: str,
        password: str,
        created: datetime | str | None = None,
        lastonline: datetime | str | None = None,
        description: str = "Hi! I just joined Roblox!",
        accountstatus: int = 1,
        TOTPEnabled: bool = False,
        force_user_id: int | None = None,
    ) -> int:
        created = self._normalise_timestamp(created)
        lastonline = self._normalise_timestamp(lastonline)

        if force_user_id is None:
            self.sqlite.execute(
                f"""
                INSERT INTO "{self.TABLE_NAME}"
                (
                    {self.field.USERNAME.value},
                    {self.field.PASSWORD.value},
                    {self.field.CREATED.value},
                    {self.field.DESCRIPTION.value},
                    {self.field.LASTONLINE.value},
                    {self.field.ACCOUNTSTATUS.value},
                    {self.field.TOTP_ENABLED.value}
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    username,
                    password,
                    created,
                    description,
                    lastonline,
                    accountstatus,
                    TOTPEnabled,
                ),
            )
            result = self.sqlite.execute_and_fetch("SELECT last_insert_rowid()")
            user_id = self.unwrap_result(result, only_first_field=True)
            assert isinstance(user_id, int)
            return user_id

        self.sqlite.execute(
            f"""
            INSERT INTO "{self.TABLE_NAME}"
            (
                {self.field.ID.value},
                {self.field.USERNAME.value},
                {self.field.PASSWORD.value},
                {self.field.CREATED.value},
                {self.field.DESCRIPTION.value},
                {self.field.LASTONLINE.value},
                {self.field.ACCOUNTSTATUS.value},
                {self.field.TOTP_ENABLED.value}
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT({self.field.ID.value})
            DO UPDATE SET
                {self.field.USERNAME.value} = excluded.{self.field.USERNAME.value},
                {self.field.PASSWORD.value} = excluded.{self.field.PASSWORD.value},
                {self.field.CREATED.value} = excluded.{self.field.CREATED.value},
                {self.field.DESCRIPTION.value} = excluded.{self.field.DESCRIPTION.value},
                {self.field.LASTONLINE.value} = excluded.{self.field.LASTONLINE.value},
                {self.field.ACCOUNTSTATUS.value} = excluded.{self.field.ACCOUNTSTATUS.value},
                {self.field.TOTP_ENABLED.value} = excluded.{self.field.TOTP_ENABLED.value}
            """,
            (
                force_user_id,
                username,
                password,
                created,
                description,
                lastonline,
                accountstatus,
                TOTPEnabled,
            ),
        )
        return force_user_id

    def _build_object_from_row(self, user_id: int, row) -> user_item | None:
        if row is None:
            return None

        return user_item(
            id=user_id,
            username=str(row[0]),
            password=str(row[1]),
            created=str(row[2]),
            description=str(row[3]),
            lastonline=str(row[4]),
            accountstatus=int(row[5]),
            TOTPEnabled=bool(row[6]),
        )

    def check(
        self,
        user_id: int,
    ) -> tuple[
        str,
        str,
        str,
        str,
        str,
        int,
        bool,
    ] | None:
        result = self.sqlite.execute_and_fetch(
            query=f"""
            SELECT
            {self.field.USERNAME.value},
            {self.field.PASSWORD.value},
            {self.field.CREATED.value},
            {self.field.DESCRIPTION.value},
            {self.field.LASTONLINE.value},
            {self.field.ACCOUNTSTATUS.value},
            {self.field.TOTP_ENABLED.value}

            FROM "{self.TABLE_NAME}"
            WHERE {self.field.ID.value} = ?
            """,
            values=(user_id,),
        )
        row = self.unwrap_result(result)
        if row is None:
            return None

        return (
            str(row[0]),
            str(row[1]),
            str(row[2]),
            str(row[3]),
            str(row[4]),
            int(row[5]),
            bool(row[6]),
        )

    def check_from_username(
        self,
        username: str,
    ) -> tuple[
        int,
        str,
        str,
        str,
        str,
        int,
        bool,
    ] | None:
        result = self.sqlite.execute_and_fetch(
            query=f"""
            SELECT
            {self.field.ID.value},
            {self.field.PASSWORD.value},
            {self.field.CREATED.value},
            {self.field.DESCRIPTION.value},
            {self.field.LASTONLINE.value},
            {self.field.ACCOUNTSTATUS.value},
            {self.field.TOTP_ENABLED.value}

            FROM "{self.TABLE_NAME}"
            WHERE {self.field.USERNAME.value} = ?
            """,
            values=(username,),
        )
        row = self.unwrap_result(result)
        if row is None:
            return None

        return (
            int(row[0]),
            str(row[1]),
            str(row[2]),
            str(row[3]),
            str(row[4]),
            int(row[5]),
            bool(row[6]),
        )

    def get_id_from_username(self, username: str) -> int | None:
        result = self.sqlite.execute_and_fetch(
            query=f"""
            SELECT {self.field.ID.value}
            FROM "{self.TABLE_NAME}"
            WHERE {self.field.USERNAME.value} = ?
            """,
            values=(username,),
        )
        return self.unwrap_result(result, only_first_field=True)

    def check_object(self, user_id: int) -> user_item | None:
        row = self.check(user_id)
        return self._build_object_from_row(user_id, row)

    def check_object_from_username(self, username: str) -> user_item | None:
        row = self.check_from_username(username)
        if row is None:
            return None

        return user_item(
            id=int(row[0]),
            username=username,
            password=str(row[1]),
            created=str(row[2]),
            description=str(row[3]),
            lastonline=str(row[4]),
            accountstatus=int(row[5]),
            TOTPEnabled=bool(row[6]),
        )

    def update_lastonline(
        self,
        user_id: int,
        lastonline: datetime | str | None = None,
    ) -> None:
        self.sqlite.execute(
            f"""
            UPDATE "{self.TABLE_NAME}"
            SET {self.field.LASTONLINE.value} = ?
            WHERE {self.field.ID.value} = ?
            """,
            (
                self._normalise_timestamp(lastonline),
                user_id,
            ),
        )

    def set_password(
        self,
        user_id: int,
        password: str,
    ) -> None:
        self.sqlite.execute(
            f"""
            UPDATE "{self.TABLE_NAME}"
            SET {self.field.PASSWORD.value} = ?
            WHERE {self.field.ID.value} = ?
            """,
            (
                password,
                user_id,
            ),
        )
