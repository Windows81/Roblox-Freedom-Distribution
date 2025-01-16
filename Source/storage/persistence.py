from . import _logic
import enum
import json


class database(_logic.sqlite_connector_base):
    TABLE_NAME = "persistence"

    class field(enum.Enum):
        SCOPE = '"scope"'
        TARGET = '"target"'
        KEY = '"key"'
        VALUE = '"value"'

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
        self.sqlite.commit()

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
        self.sqlite.commit()

    def get(self, scope: str, target: str, key: str):
        query = f"""
        SELECT {self.field.VALUE.value}
        FROM {self.TABLE_NAME}
        WHERE {self.field.SCOPE.value} = ?
        AND {self.field.TARGET.value} = ?
        AND {self.field.KEY.value} = ?
        """
        result = self.sqlite.execute(query, (scope, target, key)).fetchone()
        if result is None:
            return None
        return json.loads(result[0])

    def query_sorted_data(
        self,
        place_id: int,
        scope: str,
        key: str,
        ascending: bool = True,
        min_value: int | None = None,
        max_value: int | None = None,
        start: int = 1,
        size: int = 50
    ) -> dict:
        query = f"""
        WITH parsed_values AS (
            SELECT
                {self.field.TARGET.value} as name,
                CAST(JSON_EXTRACT({self.field.VALUE.value}, '$') AS INTEGER) as value
            FROM {self.TABLE_NAME}
            WHERE {self.field.SCOPE.value} = ?
            AND {self.field.KEY.value} = ?
            AND JSON_VALID({self.field.VALUE.value})
            AND CAST(JSON_EXTRACT({self.field.VALUE.value}, '$') AS INTEGER) IS NOT NULL
        """

        params = [scope, key]

        if min_value is not None:
            query += f" AND CAST(JSON_EXTRACT({self.field.VALUE.value}, '$') AS INTEGER) >= ?"
            params.append(min_value)

        if max_value is not None:
            query += f" AND CAST(JSON_EXTRACT({self.field.VALUE.value}, '$') AS INTEGER) < ?"
            params.append(max_value)

        query += f"""
        )
        SELECT name, value
        FROM parsed_values
        ORDER BY value {'ASC' if ascending else 'DESC'}
        LIMIT ? OFFSET ?
        """
        params.extend([size + 1, start - 1])

        results = self.sqlite.execute(query, params).fetchall()

        has_more = len(results) > size
        items = results[:size]

        next_key = start + size if has_more else None
        items_list = [{"name": str(row[0]), "value": row[1]} for row in items]

        return {
            "items": items_list,
            "has_next": has_more,
            "next_key": next_key
        }
