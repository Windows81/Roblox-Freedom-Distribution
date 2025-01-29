import sqlite_worker


class sqlite_connector_base:
    TABLE_NAME: str

    def __init__(
            self,
            sqlite: sqlite_worker.SqliteWorker,
            is_first_time: bool) -> None:
        super().__init__()
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
