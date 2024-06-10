import sqlite3
import os.path

from . import (
    players,
    persistence,
)


class storager:
    def __init__(self, path: str, force_init: bool) -> None:
        is_first_time = force_init or not os.path.isfile(path)
        self.sqlite = sqlite3.connect(path, check_same_thread=False)
        self.players = players.database(
            self.sqlite,
            is_first_time,
        )
        self.persistence = persistence.database(
            self.sqlite,
            is_first_time,
        )
