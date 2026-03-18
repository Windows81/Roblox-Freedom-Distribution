import sqlite_worker
import os.path

from . import (
    asset,
    players,
    persistence,
    badges,
    funds,
    gamepasses,
    devproducts,
    place,
    placeicon,
    universe,
)


class storager:
    def __init__(
        self,
        path: str,
        force_init: bool,
    ) -> None:
        super().__init__()
        self.is_first_time = force_init or not os.path.isfile(path)
        self.sqlite = sqlite_worker.SqliteWorker(path)

        arg_list = (
            self.sqlite,
            self.is_first_time,
        )

        self.asset = asset.database(*arg_list)
        self.players = players.database(*arg_list)
        self.persistence = persistence.database(*arg_list)
        self.badges = badges.database(*arg_list)
        self.funds = funds.database(*arg_list)
        self.gamepasses = gamepasses.database(*arg_list)
        self.devproducts = devproducts.database(*arg_list)
        self.place = place.database(*arg_list)
        self.place.asset_db = self.asset
        self.placeicon = placeicon.database(*arg_list)
        self.universe = universe.database(*arg_list)
