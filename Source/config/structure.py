from typing_extensions import Callable, Optional
from . import base_types
import util.versions
import util.resource
import enum


class chat_style(enum.Enum):
    CLASSIC_CHAT = "Classic"
    BUBBLE_CHAT = "Bubble"
    CLASSIC_AND_BUBBLE_CHAT = "ClassicAndBubble"


class avatar_type(enum.Enum):
    R6 = "R6"
    R15 = "R15"


class config_type(base_types.allocateable):
    '''
    Configuration specification, according by default to "GameConfig.toml".
    '''
    class server_assignment(base_types.allocateable):
        class players(base_types.allocateable):
            maximum: int
            preferred: int

        class instances(base_types.allocateable):
            count: int

    class game_setup(base_types.allocateable):
        place_path: Optional[base_types.allocateable.path]
        icon_path: base_types.allocateable.path
        roblox_version: util.versions.rōblox

        class creator(base_types.allocateable):
            name: str
        name: str
        description: str

    class server_core(base_types.allocateable):
        chat_style: chat_style
        retrieve_default_user_code: Callable[[float], str]
        check_user_allowed: Callable[[str, str], bool]
        retrieve_username: Callable[[str], str]
        retrieve_user_id: Callable[[str], int]
        retrieve_avatar_type: Callable[[str], avatar_type]
        retrieve_account_age: Callable[[str], int]
        filter_text: Callable[[str, str], str]
