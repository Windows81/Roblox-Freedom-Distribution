import dataclasses
from datetime import datetime
from typing import override
import enum

from . import _logic
from enums.AssetType import AssetType


@dataclasses.dataclass
class asset_item:
    id: int
    roblox_asset_id: int | None
    name: str
    description: str
    created_at: str
    updated_at: str
    asset_type: AssetType
    asset_genre: int
    creator_type: int
    creator_id: int
    moderation_status: int
    is_for_sale: bool
    price_robux: int
    price_tix: int
    is_limited: bool
    is_limited_unique: bool
    serial_count: int
    sale_count: int
    offsale_at: str | None


class database(_logic.sqlite_connector_base):
    TABLE_NAME = "asset"

    class field(enum.Enum):
        ID = '"id"'
        ROBLOX_ASSET_ID = '"roblox_asset_id"'
        NAME = '"name"'
        DESCRIPTION = '"description"'
        CREATED_AT = '"created_at"'
        UPDATED_AT = '"updated_at"'
        ASSET_TYPE = '"asset_type"'
        ASSET_GENRE = '"asset_genre"'
        CREATOR_TYPE = '"creator_type"'
        CREATOR_ID = '"creator_id"'
        MODERATION_STATUS = '"moderation_status"'
        IS_FOR_SALE = '"is_for_sale"'
        PRICE_ROBUX = '"price_robux"'
        PRICE_TIX = '"price_tix"'
        IS_LIMITED = '"is_limited"'
        IS_LIMITED_UNIQUE = '"is_limited_unique"'
        SERIAL_COUNT = '"serial_count"'
        SALE_COUNT = '"sale_count"'
        OFFSALE_AT = '"offsale_at"'

    @override
    def first_time_setup(self) -> None:
        self.sqlite.execute(
            f"""
            CREATE TABLE IF NOT EXISTS "{self.TABLE_NAME}" (
                {self.field.ID.value} INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                {self.field.ROBLOX_ASSET_ID.value} INTEGER,
                {self.field.NAME.value} TEXT NOT NULL,
                {self.field.DESCRIPTION.value} TEXT NOT NULL,
                {self.field.CREATED_AT.value} DATETIME NOT NULL,
                {self.field.UPDATED_AT.value} DATETIME NOT NULL,
                {self.field.ASSET_TYPE.value} INTEGER NOT NULL,
                {self.field.ASSET_GENRE.value} INTEGER NOT NULL,
                {self.field.CREATOR_TYPE.value} INTEGER NOT NULL,
                {self.field.CREATOR_ID.value} INTEGER NOT NULL,
                {self.field.MODERATION_STATUS.value} INTEGER NOT NULL,
                {self.field.IS_FOR_SALE.value} BOOLEAN NOT NULL DEFAULT FALSE,
                {self.field.PRICE_ROBUX.value} INTEGER NOT NULL DEFAULT 0,
                {self.field.PRICE_TIX.value} INTEGER NOT NULL DEFAULT 0,
                {self.field.IS_LIMITED.value} BOOLEAN NOT NULL DEFAULT FALSE,
                {self.field.IS_LIMITED_UNIQUE.value} BOOLEAN NOT NULL DEFAULT FALSE,
                {self.field.SERIAL_COUNT.value} INTEGER NOT NULL DEFAULT 0,
                {self.field.SALE_COUNT.value} INTEGER NOT NULL DEFAULT 0,
                {self.field.OFFSALE_AT.value} DATETIME
            );
            """,
        )
        self.sqlite.execute(
            f"""
            CREATE INDEX IF NOT EXISTS "idx_{self.TABLE_NAME}_roblox_asset_id"
            ON "{self.TABLE_NAME}" ({self.field.ROBLOX_ASSET_ID.value});
            """,
        )
        self.sqlite.execute(
            f"""
            CREATE INDEX IF NOT EXISTS "idx_{self.TABLE_NAME}_asset_type"
            ON "{self.TABLE_NAME}" ({self.field.ASSET_TYPE.value});
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
            CREATE INDEX IF NOT EXISTS "idx_{self.TABLE_NAME}_moderation_status"
            ON "{self.TABLE_NAME}" ({self.field.MODERATION_STATUS.value});
            """,
        )
        self.sqlite.execute(
            f"""
            CREATE INDEX IF NOT EXISTS "idx_{self.TABLE_NAME}_is_for_sale"
            ON "{self.TABLE_NAME}" ({self.field.IS_FOR_SALE.value});
            """,
        )
        self.sqlite.execute(
            f"""
            CREATE INDEX IF NOT EXISTS "idx_{self.TABLE_NAME}_is_limited"
            ON "{self.TABLE_NAME}" ({self.field.IS_LIMITED.value});
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
        roblox_asset_id: int | None = None,
        name: str = "Asset",
        description: str = "",
        created_at: datetime | str | None = None,
        updated_at: datetime | str | None = None,
        asset_type: AssetType | int = AssetType.Image,
        asset_genre: int = 0,
        creator_type: int = 0,
        creator_id: int = 1,
        moderation_status: int = 1,
        is_for_sale: bool = False,
        price_robux: int = 0,
        price_tix: int = 0,
        is_limited: bool = False,
        is_limited_unique: bool = False,
        serial_count: int = 0,
        sale_count: int = 0,
        offsale_at: datetime | str | None = None,
        force_asset_id: int | None = None,
    ) -> int:
        if isinstance(asset_type, AssetType):
            asset_type = asset_type.value

        created_at = self._normalise_timestamp(created_at)
        updated_at = self._normalise_timestamp(updated_at)
        offsale_at = (
            self._normalise_timestamp(offsale_at)
            if offsale_at is not None else
            None
        )

        if force_asset_id is None:
            self.sqlite.execute(
                f"""
                INSERT INTO "{self.TABLE_NAME}"
                (
                    {self.field.ROBLOX_ASSET_ID.value},
                    {self.field.NAME.value},
                    {self.field.DESCRIPTION.value},
                    {self.field.CREATED_AT.value},
                    {self.field.UPDATED_AT.value},
                    {self.field.ASSET_TYPE.value},
                    {self.field.ASSET_GENRE.value},
                    {self.field.CREATOR_TYPE.value},
                    {self.field.CREATOR_ID.value},
                    {self.field.MODERATION_STATUS.value},
                    {self.field.IS_FOR_SALE.value},
                    {self.field.PRICE_ROBUX.value},
                    {self.field.PRICE_TIX.value},
                    {self.field.IS_LIMITED.value},
                    {self.field.IS_LIMITED_UNIQUE.value},
                    {self.field.SERIAL_COUNT.value},
                    {self.field.SALE_COUNT.value},
                    {self.field.OFFSALE_AT.value}
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    roblox_asset_id,
                    name,
                    description,
                    created_at,
                    updated_at,
                    asset_type,
                    asset_genre,
                    creator_type,
                    creator_id,
                    moderation_status,
                    is_for_sale,
                    price_robux,
                    price_tix,
                    is_limited,
                    is_limited_unique,
                    serial_count,
                    sale_count,
                    offsale_at,
                ),
            )
            result = self.sqlite.execute_and_fetch("SELECT last_insert_rowid()")
            asset_id = self.unwrap_result(result, only_first_field=True)
            assert isinstance(asset_id, int)
            return asset_id

        self.sqlite.execute(
            f"""
            INSERT INTO "{self.TABLE_NAME}"
            (
                {self.field.ID.value},
                {self.field.ROBLOX_ASSET_ID.value},
                {self.field.NAME.value},
                {self.field.DESCRIPTION.value},
                {self.field.CREATED_AT.value},
                {self.field.UPDATED_AT.value},
                {self.field.ASSET_TYPE.value},
                {self.field.ASSET_GENRE.value},
                {self.field.CREATOR_TYPE.value},
                {self.field.CREATOR_ID.value},
                {self.field.MODERATION_STATUS.value},
                {self.field.IS_FOR_SALE.value},
                {self.field.PRICE_ROBUX.value},
                {self.field.PRICE_TIX.value},
                {self.field.IS_LIMITED.value},
                {self.field.IS_LIMITED_UNIQUE.value},
                {self.field.SERIAL_COUNT.value},
                {self.field.SALE_COUNT.value},
                {self.field.OFFSALE_AT.value}
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT({self.field.ID.value})
            DO UPDATE SET
                {self.field.ROBLOX_ASSET_ID.value} = excluded.{self.field.ROBLOX_ASSET_ID.value},
                {self.field.NAME.value} = excluded.{self.field.NAME.value},
                {self.field.DESCRIPTION.value} = excluded.{self.field.DESCRIPTION.value},
                {self.field.CREATED_AT.value} = excluded.{self.field.CREATED_AT.value},
                {self.field.UPDATED_AT.value} = excluded.{self.field.UPDATED_AT.value},
                {self.field.ASSET_TYPE.value} = excluded.{self.field.ASSET_TYPE.value},
                {self.field.ASSET_GENRE.value} = excluded.{self.field.ASSET_GENRE.value},
                {self.field.CREATOR_TYPE.value} = excluded.{self.field.CREATOR_TYPE.value},
                {self.field.CREATOR_ID.value} = excluded.{self.field.CREATOR_ID.value},
                {self.field.MODERATION_STATUS.value} = excluded.{self.field.MODERATION_STATUS.value},
                {self.field.IS_FOR_SALE.value} = excluded.{self.field.IS_FOR_SALE.value},
                {self.field.PRICE_ROBUX.value} = excluded.{self.field.PRICE_ROBUX.value},
                {self.field.PRICE_TIX.value} = excluded.{self.field.PRICE_TIX.value},
                {self.field.IS_LIMITED.value} = excluded.{self.field.IS_LIMITED.value},
                {self.field.IS_LIMITED_UNIQUE.value} = excluded.{self.field.IS_LIMITED_UNIQUE.value},
                {self.field.SERIAL_COUNT.value} = excluded.{self.field.SERIAL_COUNT.value},
                {self.field.SALE_COUNT.value} = excluded.{self.field.SALE_COUNT.value},
                {self.field.OFFSALE_AT.value} = excluded.{self.field.OFFSALE_AT.value}
            """,
            (
                force_asset_id,
                roblox_asset_id,
                name,
                description,
                created_at,
                updated_at,
                asset_type,
                asset_genre,
                creator_type,
                creator_id,
                moderation_status,
                is_for_sale,
                price_robux,
                price_tix,
                is_limited,
                is_limited_unique,
                serial_count,
                sale_count,
                offsale_at,
            ),
        )
        return force_asset_id

    def _build_object_from_row(self, asset_id: int, result) -> asset_item | None:
        row = self.unwrap_result(result)
        if row is None:
            return None

        return asset_item(
            id=asset_id,
            roblox_asset_id=row[0],
            name=str(row[1]),
            description=str(row[2]),
            created_at=str(row[3]),
            updated_at=str(row[4]),
            asset_type=AssetType(row[5]),
            asset_genre=int(row[6]),
            creator_type=int(row[7]),
            creator_id=int(row[8]),
            moderation_status=int(row[9]),
            is_for_sale=bool(row[10]),
            price_robux=int(row[11]),
            price_tix=int(row[12]),
            is_limited=bool(row[13]),
            is_limited_unique=bool(row[14]),
            serial_count=int(row[15]),
            sale_count=int(row[16]),
            offsale_at=None if row[17] is None else str(row[17]),
        )

    def check_object(self, asset_id: int) -> asset_item | None:
        result = self.sqlite.execute_and_fetch(
            query=f"""
            SELECT
            {self.field.ROBLOX_ASSET_ID.value},
            {self.field.NAME.value},
            {self.field.DESCRIPTION.value},
            {self.field.CREATED_AT.value},
            {self.field.UPDATED_AT.value},
            {self.field.ASSET_TYPE.value},
            {self.field.ASSET_GENRE.value},
            {self.field.CREATOR_TYPE.value},
            {self.field.CREATOR_ID.value},
            {self.field.MODERATION_STATUS.value},
            {self.field.IS_FOR_SALE.value},
            {self.field.PRICE_ROBUX.value},
            {self.field.PRICE_TIX.value},
            {self.field.IS_LIMITED.value},
            {self.field.IS_LIMITED_UNIQUE.value},
            {self.field.SERIAL_COUNT.value},
            {self.field.SALE_COUNT.value},
            {self.field.OFFSALE_AT.value}

            FROM "{self.TABLE_NAME}"
            WHERE {self.field.ID.value} = ?
            """,
            values=(asset_id,),
        )
        return self._build_object_from_row(asset_id, result)

    def check_object_from_roblox_asset_id(self, roblox_asset_id: int) -> asset_item | None:
        result = self.sqlite.execute_and_fetch(
            query=f"""
            SELECT
            {self.field.ID.value},
            {self.field.NAME.value},
            {self.field.DESCRIPTION.value},
            {self.field.CREATED_AT.value},
            {self.field.UPDATED_AT.value},
            {self.field.ASSET_TYPE.value},
            {self.field.ASSET_GENRE.value},
            {self.field.CREATOR_TYPE.value},
            {self.field.CREATOR_ID.value},
            {self.field.MODERATION_STATUS.value},
            {self.field.IS_FOR_SALE.value},
            {self.field.PRICE_ROBUX.value},
            {self.field.PRICE_TIX.value},
            {self.field.IS_LIMITED.value},
            {self.field.IS_LIMITED_UNIQUE.value},
            {self.field.SERIAL_COUNT.value},
            {self.field.SALE_COUNT.value},
            {self.field.OFFSALE_AT.value}

            FROM "{self.TABLE_NAME}"
            WHERE {self.field.ROBLOX_ASSET_ID.value} = ?
            """,
            values=(roblox_asset_id,),
        )
        row = self.unwrap_result(result)
        if row is None:
            return None

        return asset_item(
            id=int(row[0]),
            roblox_asset_id=roblox_asset_id,
            name=str(row[1]),
            description=str(row[2]),
            created_at=str(row[3]),
            updated_at=str(row[4]),
            asset_type=AssetType(row[5]),
            asset_genre=int(row[6]),
            creator_type=int(row[7]),
            creator_id=int(row[8]),
            moderation_status=int(row[9]),
            is_for_sale=bool(row[10]),
            price_robux=int(row[11]),
            price_tix=int(row[12]),
            is_limited=bool(row[13]),
            is_limited_unique=bool(row[14]),
            serial_count=int(row[15]),
            sale_count=int(row[16]),
            offsale_at=None if row[17] is None else str(row[17]),
        )

    def resolve_object(self, asset_id: int) -> asset_item | None:
        return (
            self.check_object(asset_id) or
            self.check_object_from_roblox_asset_id(asset_id)
        )
