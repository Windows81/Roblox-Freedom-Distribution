from . import wrappers
import dataclasses
import enum


@dataclasses.dataclass
class gamepass:
    id_num: int
    name: str
    price: int
    icon: wrappers.uri_obj | None = None


@dataclasses.dataclass
class badge:
    id_num: int
    name: str
    icon: wrappers.uri_obj | None = None


@dataclasses.dataclass
class asset_redirect:
    def __post_init__(self):
        if sum([
            self.cmd_line is not None,
            self.raw_data is not None,
            self.uri is not None,
        ]) > 1:
            raise Exception(
                'Entries for `asset_redirects` should not have '
                'more than one of a `uri`, a pipeable `cmd_line`, or a `raw_data` chunk.'
            )
    uri: wrappers.uri_obj | None = None
    raw_data: bytes | None = None
    cmd_line: str | None = None


class gamepasses(wrappers.dicter[gamepass, int]):
    key_name = 'id_num'


class badges(wrappers.dicter[badge, int]):
    key_name = 'id_num'


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
