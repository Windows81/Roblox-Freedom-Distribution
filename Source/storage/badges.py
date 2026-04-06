import dataclasses
import enum
from typing import override

from . import _logic


@dataclasses.dataclass
class badge_award_item:
    badge_id: int
    timestamp: str


class database(_logic.sqlite_connector_base):
    TABLE_NAME = "badges"

    class field(enum.Enum):
        USER_IDEN_NUM = '"user_id_num"'
        BADGE_IDEN = '"badge_id"'
        TIMESTAMP = '"timestamp"'

    @override
    def first_time_setup(self) -> None:
        self.sqlite.execute(
            f"""
            CREATE TABLE IF NOT EXISTS "{self.TABLE_NAME}" (
                {self.field.USER_IDEN_NUM.value} INTEGER NOT NULL,
                {self.field.BADGE_IDEN.value} INTEGER NOT NULL,
                {self.field.TIMESTAMP.value} DATETIME DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY(
                    {self.field.USER_IDEN_NUM.value},
                    {self.field.BADGE_IDEN.value}
                ) ON CONFLICT IGNORE
            );
            """,
        )

    def award(self, user_id_num: int, badge_id: int) -> None:
        self.sqlite.execute(
            f"""
            INSERT INTO "{self.TABLE_NAME}"
            (
                {self.field.USER_IDEN_NUM.value},
                {self.field.BADGE_IDEN.value}
            )
            VALUES (?, ?)
            """,
            (user_id_num, badge_id),
        )

    def check(self, user_id_num: int, badge_id: int) -> str | None:
        result = self.sqlite.execute_and_fetch(
            query=f"""
            SELECT
            {self.field.TIMESTAMP.value}

            FROM "{self.TABLE_NAME}"
            WHERE {self.field.USER_IDEN_NUM.value} = ?
            AND {self.field.BADGE_IDEN.value} = ?
            """,
            values=(user_id_num, badge_id),
        )
        return self.unwrap_result(result, only_first_field=True)

    def list_for_user(
        self,
        user_id_num: int,
        limit: int,
        offset: int,
        descending: bool = False,
    ) -> list[badge_award_item]:
        order_by = (
            f"{self.field.BADGE_IDEN.value} DESC, {self.field.TIMESTAMP.value} DESC"
            if descending else
            f"{self.field.BADGE_IDEN.value} ASC, {self.field.TIMESTAMP.value} ASC"
        )
        results = self.sqlite.execute_and_fetch(
            query=f"""
            SELECT
            {self.field.BADGE_IDEN.value},
            {self.field.TIMESTAMP.value}

            FROM "{self.TABLE_NAME}"
            WHERE {self.field.USER_IDEN_NUM.value} = ?
            ORDER BY {order_by}
            LIMIT ? OFFSET ?
            """,
            values=(user_id_num, limit, offset),
        )
        assert results is not None
        return [
            badge_award_item(
                badge_id=int(row[0]),
                timestamp=str(row[1]),
            )
            for row in results
        ]

    def get_badge_statistics(self, badge_id: int) -> tuple[int, int]:
        result = self.sqlite.execute_and_fetch(
            query=f"""
            SELECT
            COUNT(*),
            COALESCE(SUM(
                CASE
                    WHEN {self.field.TIMESTAMP.value} >= datetime('now', '-1 day')
                    THEN 1
                    ELSE 0
                END
            ), 0)

            FROM "{self.TABLE_NAME}"
            WHERE {self.field.BADGE_IDEN.value} = ?
            """,
            values=(badge_id,),
        )
        row = self.unwrap_result(result)
        if row is None:
            return (0, 0)
        return (int(row[0]), int(row[1]))
