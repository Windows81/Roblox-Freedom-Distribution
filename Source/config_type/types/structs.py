from . import wrappers
import dataclasses
import enum


@dataclasses.dataclass
class gamepass:
    id_num: int
    name: str
    price: int
    icon: wrappers.uri_obj | None = None


class gamepasses(wrappers.dicter[int, gamepass]):
    key_name = 'id_num'


@dataclasses.dataclass
class dev_product:
    id_num: int
    name: str
    price: int
    icon: wrappers.uri_obj | None = None


class dev_products(wrappers.dicter[int, dev_product]):
    key_name = 'id_num'


@dataclasses.dataclass
class badge:
    id_num: int
    name: str
    icon: wrappers.uri_obj | None = None


class badges(wrappers.dicter[int, badge]):
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


@dataclasses.dataclass
class avatar_data:
    type: avatar_type
    items: list[int]
    scales: avatar_scales
    colors: avatar_colors
