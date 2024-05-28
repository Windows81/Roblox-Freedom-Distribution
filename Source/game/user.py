import config._main


class user_dict(dict[int, str]):
    def __init__(self, game_config: config._main.obj_type):
        super().__init__()
        self.game_config = game_config

    def add_user(self, user_code: str) -> int | None:
        '''
        Adds a user code to the ID-to-user-code index.
        '''
        user_id = self.get_id_num_from_code(user_code)
        if not user_id:
            return None
        self[user_id] = user_code
        return user_id

    def sanitise_id_num(self, id_num: str | int | None) -> int | None:
        if not id_num:
            return None
        return int(id_num)

    def get_code_from_id_num(self, user_id: int) -> str | None:
        return self.get(user_id, None)

    def get_id_num_from_code(self, user_code: str) -> int | None:
        return self.game_config.server_core.retrieve_user_id(user_code)
