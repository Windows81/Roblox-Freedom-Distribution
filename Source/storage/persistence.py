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
        self.sqlite.execute(
            f"""
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
            """,
        )
        self.sqlite.commit()

    def set(self, scope: str, target: str, key: str, value) -> None:
        value_str = json.dumps(value)
        self.sqlite.execute(
            f"""
            INSERT INTO ?
            (
                {self.field.SCOPE.value},
                {self.field.TARGET.value},
                {self.field.KEY.value},
                {self.field.VALUE.value}
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                self.TABLE_NAME,
                scope,
                target,
                key,
                value_str,
            ),
        )
        self.sqlite.commit()

    def get(self, scope: str, target: str, key: str):
        result: dict | None = self.sqlite.execute(
            f"""
            SELECT
            {self.field.VALUE.value}

            FROM ?
            WHERE {self.field.SCOPE.value} = ?
            AND {self.field.TARGET.value} = ?
            AND {self.field.KEY.value} = ?
            """,
            (
                self.TABLE_NAME,
                scope,
                target,
                key,
            )
        ).fetchone()
        if result is None:
            return None

        value = result[0]
        return json.loads(value)

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
        """
        Query sorted data from the persistence database with pagination and value range filtering.

        Args:
            place_id: The place ID to filter by (stored in target field)
            scope: The scope to filter by
            key: The key to filter by
            ascending: Sort direction (True for ascending, False for descending)
            min_value: Minimum value to include (inclusive)
            max_value: Maximum value to exclude (exclusive)
            start: Starting position for pagination (1-based)
            size: Number of items to return

        Returns:
            dict with keys:
                items: List of dict with 'name' and 'value' keys
                has_next: Boolean indicating if there are more results
                next_key: Next starting position for pagination
        """
        # Build the base query
        query = f"""
            WITH parsed_values AS (
                SELECT
                    {self.field.TARGET.value} as name,
                    CAST(JSON_EXTRACT({self.field.VALUE.value}, '$') AS INTEGER) as value
                FROM "{self.TABLE_NAME}"
                WHERE {self.field.SCOPE.value} = ?
                AND {self.field.KEY.value} = ?
                AND JSON_VALID({self.field.VALUE.value})
                AND CAST(JSON_EXTRACT({self.field.VALUE.value}, '$') AS INTEGER) IS NOT NULL
        """

        params: list = [scope, key]

        # Add value range conditions if specified
        if min_value is not None:
            query += f" AND CAST(JSON_EXTRACT({
                self.field.VALUE.value}, '$') AS INTEGER) >= ?"
            params.append(min_value)

        if max_value is not None:
            query += f" AND CAST(JSON_EXTRACT({
                self.field.VALUE.value}, '$') AS INTEGER) < ?"
            params.append(max_value)

        # Close the CTE and add sorting and pagination
        query += f"""
            )
            SELECT name, value
            FROM parsed_values
            ORDER BY value {'ASC' if ascending else 'DESC'}
            LIMIT ? OFFSET ?
        """

        # Add pagination parameters
        # +1 to check if there are more results
        params.extend([size + 1, start - 1])

        # Execute query
        results = self.sqlite.execute(query, params).fetchall()

        # Process results
        has_more = len(results) > size
        # Trim extra item used to check for more results
        items = results[:size]

        # Calculate next key if there are more results
        next_key = start + size if has_more else None

        # Convert results to list of dicts
        items_list = [{"name": str(row[0]), "value": row[1]} for row in items]

        return {
            "items": items_list,
            "has_next": has_more,
            "next_key": next_key
        }
