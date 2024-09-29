from collections import defaultdict
import sqlite3
import os.path

from . import (
    players,
    persistence,
    badges,
    funds,
    gamepasses,
)


class obj_type:
    '''
    In charge of managing SQLite databases.
    '''

    def __init__(
        self,
        path: str,
        force_init: bool,
    ) -> None:
        self.is_first_time = force_init or not os.path.isfile(path)
        self.sqlite = sqlite3.connect(path, check_same_thread=False)

        arg_list = (
            self.sqlite,
            self.is_first_time,
        )

        self.players = players.database(*arg_list)
        self.persistence = persistence.database(*arg_list)
        self.badges = badges.database(*arg_list)
        self.funds = funds.database(*arg_list)
        self.gamepasses = gamepasses.database(*arg_list)


class group_type:
    def __init__(self) -> None:
        self.can_force_init = defaultdict[str, bool](lambda: True)
        self.storager_dict = dict[str, obj_type]()
        self.storager_list = list[obj_type]()

    def add(
        self,
        path: str,
        force_init: bool,
    ) -> obj_type:
        # Makes it so that `force_init` can't be True for more than one `storager` of the same path.
        if self.can_force_init[path] == False and force_init:
            force_init = self.can_force_init[path] = False

        # Checks if a storager is already assigned to the path; else make a new one.
        result = self.storager_dict.setdefault(
            path, obj_type(path, force_init),
        )
        self.storager_list.append(result)
        return result
