import sqlite3


class sqlite_connector_base:
    TABLE_NAME: str

    def __init__(
            self,
            sqlite: sqlite3.Connection,
            is_first_time: bool) -> None:
        self.sqlite = sqlite
        if is_first_time:
            self.drop_existing()
        self.first_time_setup()

    def drop_existing(self) -> None:
        self.sqlite.execute(
            f"""
            DROP TABLE IF EXISTS "{self.TABLE_NAME}"
            """,
        )

    def first_time_setup(self) -> None:
        raise NotImplementedError()
