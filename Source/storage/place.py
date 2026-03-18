import dataclasses
from typing import TYPE_CHECKING, override
import enum

from . import _logic
from enums.ChatStyle import ChatStyle
from enums.PlaceRigChoice import PlaceRigChoice
from enums.PlaceYear import PlaceYear

if TYPE_CHECKING:
    from .asset import asset_item


@dataclasses.dataclass
class place_item:
    placeid: int
    visitcount: int
    is_public: bool
    maxplayers: int
    placeyear: PlaceYear
    featured: bool
    bc_required: bool
    rig_choice: PlaceRigChoice
    chat_style: ChatStyle
    min_account_age: int
    parent_universe_id: int | None
    assetObj: 'asset_item | None' = None


class database(_logic.sqlite_connector_base):
    TABLE_NAME = "place"
    asset_db = None

    class field(enum.Enum):
        PLACE_ID = '"placeid"'
        VISIT_COUNT = '"visitcount"'
        IS_PUBLIC = '"is_public"'
        MAX_PLAYERS = '"maxplayers"'
        PLACE_YEAR = '"placeyear"'
        FEATURED = '"featured"'
        BC_REQUIRED = '"bc_required"'
        RIG_CHOICE = '"rig_choice"'
        CHAT_STYLE = '"chat_style"'
        MIN_ACCOUNT_AGE = '"min_account_age"'
        PARENT_UNIVERSE_ID = '"parent_universe_id"'

    @override
    def first_time_setup(self) -> None:
        self.sqlite.execute(
            f"""
            CREATE TABLE IF NOT EXISTS "{self.TABLE_NAME}" (
                {self.field.PLACE_ID.value} INTEGER NOT NULL,
                {self.field.VISIT_COUNT.value} INTEGER NOT NULL DEFAULT 0,
                {self.field.IS_PUBLIC.value} BOOLEAN NOT NULL DEFAULT TRUE,
                {self.field.MAX_PLAYERS.value} INTEGER NOT NULL DEFAULT 10,
                {self.field.PLACE_YEAR.value} INTEGER NOT NULL DEFAULT {PlaceYear.Sixteen.value},
                {self.field.FEATURED.value} BOOLEAN NOT NULL DEFAULT FALSE,
                {self.field.BC_REQUIRED.value} BOOLEAN NOT NULL DEFAULT FALSE,
                {self.field.RIG_CHOICE.value} INTEGER NOT NULL DEFAULT {PlaceRigChoice.UserChoice.value},
                {self.field.CHAT_STYLE.value} INTEGER NOT NULL DEFAULT {ChatStyle.ClassicAndBubble.value},
                {self.field.MIN_ACCOUNT_AGE.value} INTEGER NOT NULL DEFAULT 0,
                {self.field.PARENT_UNIVERSE_ID.value} INTEGER,
                PRIMARY KEY(
                    {self.field.PLACE_ID.value}
                ) ON CONFLICT REPLACE
            );
            """,
        )
        self.sqlite.execute(
            f"""
            CREATE INDEX IF NOT EXISTS "idx_{self.TABLE_NAME}_featured"
            ON "{self.TABLE_NAME}" ({self.field.FEATURED.value});
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
            CREATE INDEX IF NOT EXISTS "idx_{self.TABLE_NAME}_parent_universe_id"
            ON "{self.TABLE_NAME}" ({self.field.PARENT_UNIVERSE_ID.value});
            """,
        )

    def update(
        self,
        placeid: int,
        visitcount: int = 0,
        is_public: bool = True,
        maxplayers: int = 10,
        placeyear: PlaceYear | int = PlaceYear.Sixteen,
        featured: bool = False,
        bc_required: bool = False,
        rig_choice: PlaceRigChoice | int = PlaceRigChoice.UserChoice,
        chat_style: ChatStyle | int = ChatStyle.ClassicAndBubble,
        min_account_age: int = 0,
        parent_universe_id: int | None = None,
    ) -> None:
        if isinstance(placeyear, PlaceYear):
            placeyear = placeyear.value
        if isinstance(rig_choice, PlaceRigChoice):
            rig_choice = rig_choice.value
        if isinstance(chat_style, ChatStyle):
            chat_style = chat_style.value

        self.sqlite.execute(
            f"""
            INSERT INTO "{self.TABLE_NAME}"
            (
                {self.field.PLACE_ID.value},
                {self.field.VISIT_COUNT.value},
                {self.field.IS_PUBLIC.value},
                {self.field.MAX_PLAYERS.value},
                {self.field.PLACE_YEAR.value},
                {self.field.FEATURED.value},
                {self.field.BC_REQUIRED.value},
                {self.field.RIG_CHOICE.value},
                {self.field.CHAT_STYLE.value},
                {self.field.MIN_ACCOUNT_AGE.value},
                {self.field.PARENT_UNIVERSE_ID.value}
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                placeid,
                visitcount,
                is_public,
                maxplayers,
                placeyear,
                featured,
                bc_required,
                rig_choice,
                chat_style,
                min_account_age,
                parent_universe_id,
            ),
        )

    def check(
        self,
        placeid: int,
    ) -> tuple[
        int,
        bool,
        int,
        PlaceYear,
        bool,
        bool,
        PlaceRigChoice,
        ChatStyle,
        int,
        int | None,
    ] | None:
        result = self.sqlite.execute_and_fetch(
            query=f"""
            SELECT
            {self.field.VISIT_COUNT.value},
            {self.field.IS_PUBLIC.value},
            {self.field.MAX_PLAYERS.value},
            {self.field.PLACE_YEAR.value},
            {self.field.FEATURED.value},
            {self.field.BC_REQUIRED.value},
            {self.field.RIG_CHOICE.value},
            {self.field.CHAT_STYLE.value},
            {self.field.MIN_ACCOUNT_AGE.value},
            {self.field.PARENT_UNIVERSE_ID.value}

            FROM "{self.TABLE_NAME}"
            WHERE {self.field.PLACE_ID.value} = ?
            """,
            values=(placeid,),
        )
        row = self.unwrap_result(result)
        if row is None:
            return None

        return (
            int(row[0]),
            bool(row[1]),
            int(row[2]),
            PlaceYear(row[3]),
            bool(row[4]),
            bool(row[5]),
            PlaceRigChoice(row[6]),
            ChatStyle(row[7]),
            int(row[8]),
            row[9],
        )

    def check_object(self, placeid: int) -> place_item | None:
        row = self.check(placeid)
        if row is None:
            return None

        return place_item(
            placeid=placeid,
            visitcount=row[0],
            is_public=row[1],
            maxplayers=row[2],
            placeyear=row[3],
            featured=row[4],
            bc_required=row[5],
            rig_choice=row[6],
            chat_style=row[7],
            min_account_age=row[8],
            parent_universe_id=row[9],
            assetObj=(
                self.asset_db.check_object(placeid)
                if self.asset_db is not None else
                None
            ),
        )

    def increment_visitcount(self, placeid: int, delta: int = 1) -> None:
        self.sqlite.execute(
            f"""
            INSERT INTO "{self.TABLE_NAME}"
            (
                {self.field.PLACE_ID.value},
                {self.field.VISIT_COUNT.value}
            )
            VALUES (?, ?)
            ON CONFLICT({self.field.PLACE_ID.value})
            DO UPDATE SET
                {self.field.VISIT_COUNT.value} = {self.field.VISIT_COUNT.value} + excluded.{self.field.VISIT_COUNT.value}
            """,
            (placeid, delta),
        )
