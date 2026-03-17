from typing import override
from . import _logic
import enum


class database(_logic.sqlite_connector_base):
    TABLE_NAME = "placeicon"

    class field(enum.Enum):
        PLACE_ID = '"placeid"'
        CONTENT_HASH = '"contenthash"'
        UPDATED_AT = '"updated_at"'
        MODERATION_STATUS = '"moderation_status"'

    @override
    def first_time_setup(self) -> None:
        self.sqlite.execute(
            f"""
            CREATE TABLE IF NOT EXISTS "{self.TABLE_NAME}" (
                {self.field.PLACE_ID.value} INTEGER NOT NULL,
                {self.field.CONTENT_HASH.value} TEXT,
                {self.field.UPDATED_AT.value} DATETIME,
                {self.field.MODERATION_STATUS.value} INTEGER NOT NULL DEFAULT 1,
                PRIMARY KEY(
                    {self.field.PLACE_ID.value}
                ) ON CONFLICT REPLACE
            );
            """,
        )

    def update(
        self,
        placeid: int,
        content_hash: str | None,
        updated_at: str | None,
        moderation_status: int = 1,
    ) -> None:
        self.sqlite.execute(
            f"""
            INSERT INTO "{self.TABLE_NAME}"
            (
                {self.field.PLACE_ID.value},
                {self.field.CONTENT_HASH.value},
                {self.field.UPDATED_AT.value},
                {self.field.MODERATION_STATUS.value}
            )
            VALUES (?, ?, ?, ?)
            """,
            (placeid, content_hash, updated_at, moderation_status),
        )

    def check(self, placeid: int) -> tuple[str | None, str | None, int] | None:
        result = self.sqlite.execute_and_fetch(
            query=f"""
            SELECT
            {self.field.CONTENT_HASH.value},
            {self.field.UPDATED_AT.value},
            {self.field.MODERATION_STATUS.value}

            FROM "{self.TABLE_NAME}"
            WHERE {self.field.PLACE_ID.value} = ?
            """,
            values=(placeid,),
        )
        return self.unwrap_result(result)
