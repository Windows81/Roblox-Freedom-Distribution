from typing_extensions import Callable, Type

from .types import wrappers, structs
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
            uri: wrappers.uri_obj
            enable_saveplace: bool = False

        class asset_cache(allocateable.obj_type):
            path: wrappers.path_str = './AssetCache'  # type:ignore
            clear_on_start: bool = False

        class database(allocateable.obj_type):
            path: wrappers.path_str
            clear_on_start: bool

        roblox_version: util.versions.rōblox
        startup_script: str = ''

        title: str
        description: str
        creator_name: str
        icon_path: wrappers.path_str = ''  # type:ignore

    class server_core(allocateable.obj_type):
        chat_style: structs.chat_style
        retrieve_default_user_code: Callable[[float], str]
        '''
        If the client doesn't include a user code whilst
        connecting to the server, this function is called.
        Should be a randomly-generated value.
        '''

        check_user_allowed: Callable[[str], bool] = \
            'function() return true end'  # type: ignore

        retrieve_username: Callable[[str], str]
        '''
        Only gets called the first time a new user joins.
        Otherwise, RFD checks for a cached value in the `sqlite` database.
        '''

        retrieve_user_id: Callable[[str], int]
        '''
        Only gets called the first time a new user joins.
        Otherwise, RFD checks for a cached value in the `sqlite` database.
        '''

        retrieve_avatar_type: Callable[[str], structs.avatar_type]
        '''
        Should return either `"R6"` or `"R15"` as a string.
        '''

        retrieve_avatar_items: Callable[[str], list[int]]
        '''
        List contains catalogue asset ids.
        '''

        retrieve_avatar_scales: Callable[[str], structs.avatar_scales]

        retrieve_avatar_colors: Callable[[str], structs.avatar_colors]
        '''
        TODO: support all possible brick colour codes in 2018M.
        '''

        retrieve_groups: Callable[[str], dict[str, int]]
        '''
        Key is the group id.  Value is the rank.
        '''

        retrieve_account_age: Callable[[str], int]
        filter_text: Callable[[str, str], str]

    class remote_data(allocateable.obj_type):
        gamepasses: structs.gamepasses
        badges: structs.badges
