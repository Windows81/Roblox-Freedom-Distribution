# Standard library imports
import dataclasses
import enum
import json

# Typing imports
from typing import Any, override

# Local application imports
from . import _logic



@dataclasses.dataclass
class sorted_item:
    name: str
    value: Any


@dataclasses.dataclass
class sorted_struct:
    items: list[sorted_item]
    next_key: int | None


class database(_logic.sqlite_connector_base):
    TABLE_NAME = "persistence"

    class field(enum.Enum):
        SCOPE = '"scope"'
        TARGET = '"target"'
        KEY = '"key"'
        VALUE = '"value"'

    @override
    def first_time_setup(self) -> None:
        query = f"""
        CREATE TABLE IF NOT EXISTS "{self.TABLE_NAME}" (
            {self.field.SCOPE.value} TEXT NOT NULL,
            {self.field.TARGET.value} TEXT NOT NULL,
            {self.field.KEY.value} TEXT NOT NULL,
            {self.field.VALUE.value} TEXT,
            PRIMARY KEY(
                {self.field.SCOPE.value},
                {self.field.TARGET.value},
                {self.field.KEY.value}
            ) ON CONFLICT REPLACE
        );
        """
        self.sqlite.execute(query)

    def set(self, scope: str, target: str, key: str, value) -> None:
        value_str = json.dumps(value)
        query = f"""
        INSERT INTO {self.TABLE_NAME}
        (
            {self.field.SCOPE.value},
            {self.field.TARGET.value},
            {self.field.KEY.value},
            {self.field.VALUE.value}
        )
        VALUES (?, ?, ?, ?)
        """
        self.sqlite.execute(query, (scope, target, key, value_str))

    def get(self, scope: str, target: str, key: str):
        query = f"""
        SELECT {self.field.VALUE.value}
        FROM {self.TABLE_NAME}
        WHERE {self.field.SCOPE.value} = ?
        AND {self.field.TARGET.value} = ?
        AND {self.field.KEY.value} = ?
        """
        result: list[tuple[Any]] | None = self.sqlite.fetch_results(
            self.sqlite.execute(query, (scope, target, key))
        )
        assert result is not None
        if len(result) > 0:
            return json.loads(result[0][0])
        return None

    def query_sorted_data(
        self,
        scope: str,
        key: str,
        ascending: bool = True,
        min_value: int | None = None,
        max_value: int | None = None,
        start: int = 1,
        size: int = 50
    ) -> sorted_struct:
        params: list[Any] = [scope, key]

        int_casted_skeleton = (
            "CAST(JSON_EXTRACT(%s, '$') AS INTEGER)" %
            (self.field.VALUE.value,)
        )

        value_bound_suffix = ''
        if min_value is not None:
            value_bound_suffix += f" AND {int_casted_skeleton} >= ?"
            params.append(min_value)
        if max_value is not None:
            value_bound_suffix += f" AND {int_casted_skeleton} < ?"
            params.append(max_value)
        params.extend([size + 1, start - 1])

        query = f"""
        WITH parsed_values AS (
            SELECT
                {self.field.TARGET.value} as name,
                {int_casted_skeleton} as value
            FROM {self.TABLE_NAME}
            WHERE {self.field.SCOPE.value} = ?
            AND {self.field.KEY.value} = ?
            AND JSON_VALID({self.field.VALUE.value})
            AND {int_casted_skeleton} IS NOT NULL
            {value_bound_suffix}
        )
        SELECT name, value
        FROM parsed_values
        ORDER BY value {'ASC' if ascending else 'DESC'}
        LIMIT ? OFFSET ?
        """

        results: list[list[Any]] | None = self.sqlite.fetch_results(
            self.sqlite.execute(query, params, always_return_token=True)
        )
        assert results is not None

        items_list = [
            sorted_item(
                name=str(row[0]),
                value=row[1],
            )
            for row in results[:size]
        ]

        next_key = (
            start + size
            if len(results) > size  # More keys exist if evaluated to true.
            else None
        )

        return sorted_struct(
            items=items_list,
            next_key=next_key,
        )
