from typing_extensions import Callable

from . import allocateable
from . import custom_types
import util.versions
import util.resource
import dataclasses
import enum


@dataclasses.dataclass
class avatar_colors:
    head: int
    left_arm: int
    left_leg: int
    right_arm: int
    right_leg: int
    torso: int


@dataclasses.dataclass
class avatar_scales:
    height: float
    width: float
    head: float
    depth: float
    proportion: float
    body_type: float


class chat_style(enum.Enum):
    CLASSIC_CHAT = "Classic"
    BUBBLE_CHAT = "Bubble"
    CLASSIC_AND_BUBBLE_CHAT = "ClassicAndBubble"


class avatar_type(enum.Enum):
    R6 = "R6"
    R15 = "R15"


class config_type(allocateable.obj_type):
    '''
    Configuration specification, according by default to "GameConfig.toml".
    '''
    class server_assignment(allocateable.obj_type):
        class players(allocateable.obj_type):
            maximum: int
            preferred: int

        class instances(allocateable.obj_type):
            count: int

    class game_setup(allocateable.obj_type):
        class place(allocateable.obj_type):
            path: custom_types.path_obj
            enable_saveplace: bool = False

        class asset_cache(allocateable.obj_type):
            path: custom_types.path_obj = custom_types.path_obj('./AssetCache')

        class database(allocateable.obj_type):
            path: custom_types.path_obj
            clear_on_start: bool

        class icon(allocateable.obj_type):
            path: custom_types.path_obj = custom_types.path_obj('')

        class creator(allocateable.obj_type):
            name: str

        startup_script: str = ''

        title: str
        description: str

        roblox_version: util.versions.rōblox

    class server_core(allocateable.obj_type):
        chat_style: chat_style
        retrieve_default_user_code: Callable[[float], str]
        check_user_allowed: Callable[[str], bool] = \
            'function() return true end'  # type: ignore
        retrieve_username: Callable[[str], str]
        retrieve_user_id: Callable[[str], int]
        retrieve_avatar_type: Callable[[str], avatar_type]
        retrieve_avatar_items: Callable[[str], list[str]]
        retrieve_avatar_scales: Callable[[str], avatar_scales]
        retrieve_avatar_colors: Callable[[str], avatar_colors]
        retrieve_account_age: Callable[[str], int]
        filter_text: Callable[[str, str], str]
