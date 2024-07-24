import sqlite3
import os.path

from . import (
    players,
    persistence,
    badges,
)


class storager:
    def __init__(self, path: str, force_init: bool) -> None:
        is_first_time = force_init or not os.path.isfile(path)
        self.sqlite = sqlite3.connect(path, check_same_thread=False)
        arg_list = (
            self.sqlite,
            is_first_time,
        )

        self.players = players.database(*arg_list)
        self.persistence = persistence.database(*arg_list)
        self.badges = badges.database(*arg_list)
