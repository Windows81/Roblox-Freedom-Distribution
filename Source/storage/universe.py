import dataclasses
from datetime import datetime
from typing import override
import enum

from . import _logic
from enums.PlaceRigChoice import PlaceRigChoice
from enums.PlaceYear import PlaceYear


@dataclasses.dataclass
class games_api_item:
    universe_id: int
    root_place_id: int
    creator_id: int
    creator_type: int
    created_at: str
    updated_at: str
    minimum_account_age: int
    visit_count: int


@dataclasses.dataclass
class games_api_page:
    items: list[games_api_item]
    has_next: bool


class database(_logic.sqlite_connector_base):
    TABLE_NAME = "universe"

    class field(enum.Enum):
        ID = '"id"'
        ROOT_PLACE_ID = '"root_place_id"'
        CREATOR_ID = '"creator_id"'
        CREATOR_TYPE = '"creator_type"'
        CREATED_AT = '"created_at"'
        UPDATED_AT = '"updated_at"'
        PLACE_RIG_CHOICE = '"place_rig_choice"'
        PLACE_YEAR = '"place_year"'
        IS_FEATURED = '"is_featured"'
        MINIMUM_ACCOUNT_AGE = '"minimum_account_age"'
        BC_REQUIRED = '"bc_required"'
        ALLOW_DIRECT_JOIN = '"allow_direct_join"'
        IS_PUBLIC = '"is_public"'
        MODERATION_STATUS = '"moderation_status"'
        VISIT_COUNT = '"visit_count"'

    @override
    def first_time_setup(self) -> None:
        self.sqlite.execute(
            f"""
            CREATE TABLE IF NOT EXISTS "{self.TABLE_NAME}" (
                {self.field.ID.value} INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                {self.field.ROOT_PLACE_ID.value} INTEGER NOT NULL,
                {self.field.CREATOR_ID.value} INTEGER NOT NULL,
                {self.field.CREATOR_TYPE.value} INTEGER NOT NULL,
                {self.field.CREATED_AT.value} DATETIME NOT NULL,
                {self.field.UPDATED_AT.value} DATETIME NOT NULL,
                {self.field.PLACE_RIG_CHOICE.value} INTEGER NOT NULL DEFAULT {PlaceRigChoice.UserChoice.value},
                {self.field.PLACE_YEAR.value} INTEGER NOT NULL DEFAULT {PlaceYear.Sixteen.value},
                {self.field.IS_FEATURED.value} BOOLEAN NOT NULL DEFAULT FALSE,
                {self.field.MINIMUM_ACCOUNT_AGE.value} INTEGER NOT NULL DEFAULT 0,
                {self.field.BC_REQUIRED.value} BOOLEAN NOT NULL DEFAULT FALSE,
                {self.field.ALLOW_DIRECT_JOIN.value} BOOLEAN NOT NULL DEFAULT FALSE,
                {self.field.IS_PUBLIC.value} BOOLEAN NOT NULL DEFAULT TRUE,
                {self.field.MODERATION_STATUS.value} INTEGER NOT NULL DEFAULT 0,
                {self.field.VISIT_COUNT.value} INTEGER NOT NULL DEFAULT 0,
                UNIQUE ({self.field.ROOT_PLACE_ID.value}) ON CONFLICT ABORT
            );
            """,
        )
        self.sqlite.execute(
            f"""
            CREATE INDEX IF NOT EXISTS "idx_{self.TABLE_NAME}_creator_id"
            ON "{self.TABLE_NAME}" ({self.field.CREATOR_ID.value});
            """,
        )
        self.sqlite.execute(
            f"""
            CREATE INDEX IF NOT EXISTS "idx_{self.TABLE_NAME}_is_featured"
            ON "{self.TABLE_NAME}" ({self.field.IS_FEATURED.value});
            """,
        )
        self.sqlite.execute(
            f"""
            CREATE INDEX IF NOT EXISTS "idx_{self.TABLE_NAME}_bc_required"
            ON "{self.TABLE_NAME}" ({self.field.BC_REQUIRED.value});
            """,
        )
        self.sqlite.execute(
            f"""
            CREATE INDEX IF NOT EXISTS "idx_{self.TABLE_NAME}_allow_direct_join"
            ON "{self.TABLE_NAME}" ({self.field.ALLOW_DIRECT_JOIN.value});
            """,
        )
        self.sqlite.execute(
            f"""
            CREATE INDEX IF NOT EXISTS "idx_{self.TABLE_NAME}_is_public"
            ON "{self.TABLE_NAME}" ({self.field.IS_PUBLIC.value});
            """,
        )
        self.sqlite.execute(
            f"""
            CREATE INDEX IF NOT EXISTS "idx_{self.TABLE_NAME}_moderation_status"
            ON "{self.TABLE_NAME}" ({self.field.MODERATION_STATUS.value});
            """,
        )
        self.sqlite.execute(
            f"""
            CREATE INDEX IF NOT EXISTS "idx_{self.TABLE_NAME}_visit_count"
            ON "{self.TABLE_NAME}" ({self.field.VISIT_COUNT.value});
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
        root_place_id: int,
        creator_id: int,
        creator_type: int,
        place_rig_choice: PlaceRigChoice | int = PlaceRigChoice.UserChoice,
        place_year: PlaceYear | int = PlaceYear.Sixteen,
        is_featured: bool = False,
        minimum_account_age: int = 0,
        bc_required: bool = False,
        allow_direct_join: bool = False,
        is_public: bool = True,
        moderation_status: int = 0,
        visit_count: int = 0,
        updated_at: datetime | str | None = None,
        created_at: datetime | str | None = None,
    ) -> int | None:
        if isinstance(place_rig_choice, PlaceRigChoice):
            place_rig_choice = place_rig_choice.value
        if isinstance(place_year, PlaceYear):
            place_year = place_year.value

        created_at = self._normalise_timestamp(created_at)
        updated_at = self._normalise_timestamp(updated_at)

        self.sqlite.execute(
            f"""
            INSERT INTO "{self.TABLE_NAME}"
            (
                {self.field.ROOT_PLACE_ID.value},
                {self.field.CREATOR_ID.value},
                {self.field.CREATOR_TYPE.value},
                {self.field.CREATED_AT.value},
                {self.field.UPDATED_AT.value},
                {self.field.PLACE_RIG_CHOICE.value},
                {self.field.PLACE_YEAR.value},
                {self.field.IS_FEATURED.value},
                {self.field.MINIMUM_ACCOUNT_AGE.value},
                {self.field.BC_REQUIRED.value},
                {self.field.ALLOW_DIRECT_JOIN.value},
                {self.field.IS_PUBLIC.value},
                {self.field.MODERATION_STATUS.value},
                {self.field.VISIT_COUNT.value}
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT({self.field.ROOT_PLACE_ID.value})
            DO UPDATE SET
                {self.field.CREATOR_ID.value} = excluded.{self.field.CREATOR_ID.value},
                {self.field.CREATOR_TYPE.value} = excluded.{self.field.CREATOR_TYPE.value},
                {self.field.UPDATED_AT.value} = excluded.{self.field.UPDATED_AT.value},
                {self.field.PLACE_RIG_CHOICE.value} = excluded.{self.field.PLACE_RIG_CHOICE.value},
                {self.field.PLACE_YEAR.value} = excluded.{self.field.PLACE_YEAR.value},
                {self.field.IS_FEATURED.value} = excluded.{self.field.IS_FEATURED.value},
                {self.field.MINIMUM_ACCOUNT_AGE.value} = excluded.{self.field.MINIMUM_ACCOUNT_AGE.value},
                {self.field.BC_REQUIRED.value} = excluded.{self.field.BC_REQUIRED.value},
                {self.field.ALLOW_DIRECT_JOIN.value} = excluded.{self.field.ALLOW_DIRECT_JOIN.value},
                {self.field.IS_PUBLIC.value} = excluded.{self.field.IS_PUBLIC.value},
                {self.field.MODERATION_STATUS.value} = excluded.{self.field.MODERATION_STATUS.value},
                {self.field.VISIT_COUNT.value} = excluded.{self.field.VISIT_COUNT.value}
            """,
            (
                root_place_id,
                creator_id,
                creator_type,
                created_at,
                updated_at,
                place_rig_choice,
                place_year,
                is_featured,
                minimum_account_age,
                bc_required,
                allow_direct_join,
                is_public,
                moderation_status,
                visit_count,
            ),
        )
        return self.get_id_from_root_place_id(root_place_id)

    def get_id_from_root_place_id(self, root_place_id: int) -> int | None:
        result = self.sqlite.execute_and_fetch(
            query=f"""
            SELECT {self.field.ID.value}
            FROM "{self.TABLE_NAME}"
            WHERE {self.field.ROOT_PLACE_ID.value} = ?
            """,
            values=(root_place_id,),
        )
        return self.unwrap_result(result, only_first_field=True)

    def check(
        self,
        universe_id: int,
    ) -> tuple[
        int,
        int,
        int,
        str,
        str,
        PlaceRigChoice,
        PlaceYear,
        bool,
        int,
        bool,
        bool,
        bool,
        int,
        int,
    ] | None:
        result = self.sqlite.execute_and_fetch(
            query=f"""
            SELECT
            {self.field.ROOT_PLACE_ID.value},
            {self.field.CREATOR_ID.value},
            {self.field.CREATOR_TYPE.value},
            {self.field.CREATED_AT.value},
            {self.field.UPDATED_AT.value},
            {self.field.PLACE_RIG_CHOICE.value},
            {self.field.PLACE_YEAR.value},
            {self.field.IS_FEATURED.value},
            {self.field.MINIMUM_ACCOUNT_AGE.value},
            {self.field.BC_REQUIRED.value},
            {self.field.ALLOW_DIRECT_JOIN.value},
            {self.field.IS_PUBLIC.value},
            {self.field.MODERATION_STATUS.value},
            {self.field.VISIT_COUNT.value}

            FROM "{self.TABLE_NAME}"
            WHERE {self.field.ID.value} = ?
            """,
            values=(universe_id,),
        )
        row = self.unwrap_result(result)
        if row is None:
            return None

        return (
            int(row[0]),
            int(row[1]),
            int(row[2]),
            str(row[3]),
            str(row[4]),
            PlaceRigChoice(row[5]),
            PlaceYear(row[6]),
            bool(row[7]),
            int(row[8]),
            bool(row[9]),
            bool(row[10]),
            bool(row[11]),
            int(row[12]),
            int(row[13]),
        )

    def check_from_root_place_id(
        self,
        root_place_id: int,
    ) -> tuple[
        int,
        int,
        int,
        str,
        str,
        PlaceRigChoice,
        PlaceYear,
        bool,
        int,
        bool,
        bool,
        bool,
        int,
        int,
    ] | None:
        universe_id = self.get_id_from_root_place_id(root_place_id)
        if universe_id is None:
            return None
        return self.check(universe_id)

    def increment_visit_count(self, universe_id: int, delta: int = 1) -> None:
        self.sqlite.execute(
            f"""
            UPDATE "{self.TABLE_NAME}"
            SET {self.field.VISIT_COUNT.value} = {self.field.VISIT_COUNT.value} + ?
            WHERE {self.field.ID.value} = ?
            """,
            (delta, universe_id),
        )

    def list_for_games_api(
        self,
        sort_token: str,
        start_rows: int,
        max_rows: int,
    ) -> games_api_page:
        if max_rows == 0:
            return games_api_page(items=[], has_next=False)

        where_parts = [
            f"{self.field.IS_PUBLIC.value} = TRUE",
            f"{self.field.PLACE_YEAR.value} = ?",
        ]
        query_params: list[int | str] = [PlaceYear.Twenty.value]

        if sort_token == "Featured":
            where_parts.append(f"{self.field.IS_FEATURED.value} = TRUE")

        order_by = (
            f"{self.field.UPDATED_AT.value} DESC"
            if sort_token == "RecentlyUpdated" else
            (
                f"{self.field.VISIT_COUNT.value} DESC, "
                f"{self.field.UPDATED_AT.value} DESC"
            )
        )

        query_params.extend([max_rows + 1, start_rows])
        results = self.sqlite.execute_and_fetch(
            query=f"""
            SELECT
            {self.field.ID.value},
            {self.field.ROOT_PLACE_ID.value},
            {self.field.CREATOR_ID.value},
            {self.field.CREATOR_TYPE.value},
            {self.field.CREATED_AT.value},
            {self.field.UPDATED_AT.value},
            {self.field.MINIMUM_ACCOUNT_AGE.value},
            {self.field.VISIT_COUNT.value}

            FROM "{self.TABLE_NAME}"
            WHERE {" AND ".join(where_parts)}
            ORDER BY {order_by}
            LIMIT ? OFFSET ?
            """,
            values=tuple(query_params),
        )
        assert results is not None

        items = [
            games_api_item(
                universe_id=int(row[0]),
                root_place_id=int(row[1]),
                creator_id=int(row[2]),
                creator_type=int(row[3]),
                created_at=str(row[4]),
                updated_at=str(row[5]),
                minimum_account_age=int(row[6]),
                visit_count=int(row[7]),
            )
            for row in results[:max_rows]
        ]
        return games_api_page(
            items=items,
            has_next=len(results) > max_rows,
        )
