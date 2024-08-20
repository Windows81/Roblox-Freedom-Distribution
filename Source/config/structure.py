from .types.callable import obj_type as callable
from .types import structs, wrappers
from . import allocateable
import util.versions
import util.resource


class config_type(allocateable.obj_type):
    '''
    Configuration specification, according by default to "GameConfig.toml".
    '''
    class metadata(allocateable.obj_type):
        config_version_wildcard: wrappers.rfd_version_check = "*"  # type:ignore

    class server_assignment(allocateable.obj_type):
        class players(allocateable.obj_type):
            maximum: int
            preferred: int

        class instances(allocateable.obj_type):
            count: int

    class game_setup(allocateable.obj_type):
        class place_file(allocateable.obj_type):
            rbxl_uri: wrappers.uri_obj
            enable_saveplace: bool = False

        class asset_cache(allocateable.obj_type):
            dir_path: wrappers.path_str = './AssetCache'  # type:ignore
            clear_on_start: bool = False

        class persistence(allocateable.obj_type):
            sqlite_path: wrappers.path_str
            clear_on_start: bool = False

        roblox_version: util.versions.rōblox
        startup_script: str = ''

        title: str
        description: str
        creator_name: str
        icon_path: wrappers.path_str = ''  # type:ignore

    class server_core(allocateable.obj_type):
        chat_style: structs.chat_style

        retrieve_default_user_code: callable[[float], str]

        check_user_allowed: callable[[int, str], bool] = \
            'function() return true end'  # type: ignore

        check_user_has_admin: callable[[int, str], bool] = \
            'function() return false end'  # type: ignore

        retrieve_username: callable[[str], str]

        retrieve_user_id: callable[[str], int]

        retrieve_avatar_type: callable[[int, str], structs.avatar_type]

        retrieve_avatar_items: callable[[int, str], list[int]]

        retrieve_avatar_scales: callable[[int, str], structs.avatar_scales]

        retrieve_avatar_colors: callable[[int, str], structs.avatar_colors]

        retrieve_groups: callable[[int, str], dict[str, int]] = \
            'function() return {} end'  # type: ignore

        retrieve_account_age: callable[[int, str], int]
        retrieve_default_funds: callable[[int, str], int]
        filter_text: callable[[str, int, str], str]

    class remote_data(allocateable.obj_type):
        gamepasses: structs.gamepasses = []  # type: ignore
        asset_redirects: callable[[int | str], structs.asset_redirect | None] = \
            'function() return nil end'  # type: ignore
        badges: structs.badges = []  # type: ignore
