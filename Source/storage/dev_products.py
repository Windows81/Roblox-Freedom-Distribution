from typing import override
from . import _logic
import enum


class database(_logic.sqlite_connector_base):
    TABLE_NAME = "dev_products"

    class field(enum.Enum):
        USER_ID_NUM = '"user_id_num"'
        DEV_PRODUCT_ID = '"dev_product_id"'
        PURCHASE_COUNT = '"purchase_count"'
        IS_CALLED_BACK = '"is_called_back"'
        LAST_TIMESTAMP = '"last_timestamp"'

    @override
    def first_time_setup(self) -> None:
        self.sqlite.execute(
            f"""
            CREATE TABLE IF NOT EXISTS "{self.TABLE_NAME}" (
                {self.field.USER_ID_NUM.value} INTEGER NOT NULL,
                {self.field.DEV_PRODUCT_ID.value} INTEGER NOT NULL,
                {self.field.PURCHASE_COUNT.value} INTEGER NOT NULL DEFAULT 1,
                {self.field.IS_CALLED_BACK.value} BOOLEAN NOT NULL DEFAULT FALSE,
                {self.field.LAST_TIMESTAMP.value} DATETIME DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY(
                    {self.field.USER_ID_NUM.value},
                    {self.field.DEV_PRODUCT_ID.value}
                ) ON CONFLICT REPLACE
            );
            """,
        )

    def update(self, user_id_num: int, dev_product_id: int) -> None:
        self.sqlite.execute(
            f"""
            INSERT INTO "{self.TABLE_NAME}"
            (
                {self.field.USER_ID_NUM.value},
                {self.field.DEV_PRODUCT_ID.value},
                {self.field.PURCHASE_COUNT.value}
            )
            VALUES (?, ?, 1)
            ON CONFLICT({self.field.USER_ID_NUM.value}, {self.field.DEV_PRODUCT_ID.value})
            DO UPDATE SET
                {self.field.PURCHASE_COUNT.value} = {self.field.PURCHASE_COUNT.value} + 1,
                {self.field.IS_CALLED_BACK.value} = FALSE
            """,
            (
                user_id_num,
                dev_product_id,
            ),
        )

    def receipts(self) -> list[tuple[int, int, str]]:
        passes = self.sqlite.fetch_results(self.sqlite.execute(
            f"""
            SELECT
            {self.field.USER_ID_NUM.value},
            {self.field.DEV_PRODUCT_ID.value}

            FROM "{self.TABLE_NAME}"
            WHERE {self.field.IS_CALLED_BACK.value} = FALSE
            """,
        ))
        assert passes is not None

        # Updates the dev products so as to not repeat the same ones.
        self.sqlite.execute(
            f"""
            UPDATE "{self.TABLE_NAME}"
            SET {self.field.IS_CALLED_BACK.value} = TRUE
            """,
        )

        return [
            (user_id_num, dev_product_id, f"{dev_product_id}-{user_id_num}",)
            for (user_id_num, dev_product_id) in passes
        ]

    def check(self, user_id_num: int, dev_product_id: int) -> str | None:
        result = self.sqlite.fetch_results(self.sqlite.execute(
            f"""
            SELECT
            {self.field.LAST_TIMESTAMP.value}

            FROM "{self.TABLE_NAME}"
            WHERE {self.field.USER_ID_NUM.value} = {user_id_num}
            AND {self.field.DEV_PRODUCT_ID.value} = {dev_product_id}
            """,
        ))
        assert result is not None
        if len(result) > 0:
            return result[0]
        return None
