from . import wrappers
import dataclasses
import enum


@dataclasses.dataclass
class gamepass:
    id_num: int
    name: str
    price: int
    icon: int


@dataclasses.dataclass
class badge:
    id_num: int
    name: str
    icon: int


@dataclasses.dataclass
class asset_redirect:
    id_num: int | str
    uri: wrappers.uri_obj


class gamepasses(wrappers.dicter[gamepass, int]):
    key_name = 'id_num'


class badges(wrappers.dicter[badge, int]):
    key_name = 'id_num'


class asset_redirects(wrappers.dicter[asset_redirect, int | str]):
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
