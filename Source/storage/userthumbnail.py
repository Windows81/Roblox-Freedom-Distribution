from typing import override
from . import _logic
import enum


class database(_logic.sqlite_connector_base):
    TABLE_NAME = "userthumbnail"

    class field(enum.Enum):
        USER_ID = '"userid"'
        FULL_CONTENT_HASH = '"full_contenthash"'
        HEADSHOT_CONTENT_HASH = '"headshot_contenthash"'
        UPDATED_AT = '"updated_at"'

    @override
    def first_time_setup(self) -> None:
        self.sqlite.execute(
            f"""
            CREATE TABLE IF NOT EXISTS "{self.TABLE_NAME}" (
                {self.field.USER_ID.value} INTEGER NOT NULL,
                {self.field.FULL_CONTENT_HASH.value} TEXT,
                {self.field.HEADSHOT_CONTENT_HASH.value} TEXT,
                {self.field.UPDATED_AT.value} DATETIME,
                PRIMARY KEY(
                    {self.field.USER_ID.value}
                ) ON CONFLICT REPLACE
            );
            """,
        )

    def update(
        self,
        userid: int,
        full_contenthash: str | None,
        headshot_contenthash: str | None,
        updated_at: str | None,
    ) -> None:
        self.sqlite.execute(
            f"""
            INSERT INTO "{self.TABLE_NAME}"
            (
                {self.field.USER_ID.value},
                {self.field.FULL_CONTENT_HASH.value},
                {self.field.HEADSHOT_CONTENT_HASH.value},
                {self.field.UPDATED_AT.value}
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                userid,
                full_contenthash,
                headshot_contenthash,
                updated_at,
            ),
        )

    def check(self, userid: int) -> tuple[str | None, str | None, str | None] | None:
        result = self.sqlite.execute_and_fetch(
            query=f"""
            SELECT
            {self.field.FULL_CONTENT_HASH.value},
            {self.field.HEADSHOT_CONTENT_HASH.value},
            {self.field.UPDATED_AT.value}

            FROM "{self.TABLE_NAME}"
            WHERE {self.field.USER_ID.value} = ?
            """,
            values=(userid,),
        )
        return self.unwrap_result(result)
