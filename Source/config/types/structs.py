from . import wrappers
import dataclasses
import enum


@dataclasses.dataclass
class badge:
    id_num: int
    name: str
    icon: int


@dataclasses.dataclass
class gamepass:
    id_num: int
    name: str
    icon: int


@wrappers.dicter(int, 'id_num')
class gamepasses(gamepass):
    pass


@wrappers.dicter(int, 'id_num')
class badges(badge):
    pass


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
