import dataclasses


@dataclasses.dataclass
class user_info_type:
    id_num: int
    user_code: str


class user_dict(dict[int, str]):
    def __init__(self, game_config) -> None:
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

    def resolve_user_info(self, id_num: str | int | None) -> user_info_type | None:
        id_num = self.sanitise_id_num(id_num)
        if not id_num:
            return None

        user_code = self.get_code_from_id_num(id_num)
        if not user_code:
            return None

        return user_info_type(id_num, user_code)

    def sanitise_id_num(self, id_num: str | int | None) -> int | None:
        if not id_num:
            return None
        return int(id_num)

    def get_code_from_id_num(self, user_id: int) -> str | None:
        return self.get(user_id, None)

    def get_id_num_from_code(self, user_code: str) -> int | None:
        return self.game_config.server_core.retrieve_user_id(user_code)
