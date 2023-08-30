
from game_config._logic import allocateable as A
import game_config._logic
import util.versions
import util.resource
import functools
import typing
import enum


class chat_style(enum.Enum):
    CLASSIC_CHAT = "Classic"
    BUBBLE_CHAT = "Bubble"
    CLASSIC_AND_BUBBLE_CHAT = "ClassicAndBubble"


class obj_type(game_config._logic._configtype):
    '''
    Configuration specification, according by default to "GameConfig.toml".
    '''
    class server_assignment(A):
        class players(A):
            maximum: int
            preferred: int

        class instances(A):
            count: int

    class game_setup(A):
        place_path: game_config._logic.path
        icon_path: game_config._logic.path
        roblox_version: util.versions.rōblox

    class server_core(A):
        chat_style: chat_style
        retrieve_default_user_code: typing.Callable[[float], str]
        retrieve_username: typing.Callable[[str], str]
        retrieve_user_id: typing.Callable[[str], int]
        retrieve_account_age: typing.Callable[[str], int]


@functools.cache
def get_config(path: str = util.resource.DEFAULT_CONFIG_PATH) -> obj_type:
    return obj_type(path)
