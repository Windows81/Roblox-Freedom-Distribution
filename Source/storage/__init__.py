import sqlite_worker
import os.path

from . import (
    asset,
    auth_ticket,
    auth_session,
    players,
    user,
    userthumbnail,
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
        self.auth_ticket = auth_ticket.database(*arg_list)
        self.auth_session = auth_session.database(*arg_list)
        self.players = players.database(*arg_list)
        self.user = user.database(*arg_list)
        self.userthumbnail = userthumbnail.database(*arg_list)
        self.persistence = persistence.database(*arg_list)
        self.badges = badges.database(*arg_list)
        self.funds = funds.database(*arg_list)
        self.gamepasses = gamepasses.database(*arg_list)
        self.devproducts = devproducts.database(*arg_list)
        self.place = place.database(*arg_list)
        self.place.asset_db = self.asset
        self.placeicon = placeicon.database(*arg_list)
        self.universe = universe.database(*arg_list)
