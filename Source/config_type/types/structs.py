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
class asset_redirect:
    def __post_init__(self) -> None:
        if sum([
            self.cmd_line is not None,
            self.raw_data is not None,
            self.forward_url is not None,
        ]) > 1:
            raise Exception(
                'Entries for `asset_redirects` should not have ' +
                'more than one of a `forward_url`, a pipeable `cmd_line`, or a `raw_data` chunk.'
            )
    forward_url: str | None = None
    raw_data: bytes | None = None
    cmd_line: str | None = None


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
