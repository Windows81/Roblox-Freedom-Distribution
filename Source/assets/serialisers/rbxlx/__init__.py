from functools import partial
from xml.etree import ElementTree
import enum

from . import (
    roblox_links,
)

HEADER_SIGNATURE = b'<roblox '


class method(enum.Enum):
    '''
    Why `partial`?  https://stackoverflow.com/a/58714331/6879778
    '''
    roblox_links = enum.member(partial(roblox_links.replace))
    # convert_csg = enum.member(partial(convert_csg.replace))


ALL_METHODS = set(method)


def check(data: bytes) -> bool:
    return data.startswith(HEADER_SIGNATURE)


def parse(data: bytes, methods: set[method] = ALL_METHODS) -> bytes | None:
    if not check(data):
        return
    tree = ElementTree.fromstring(data)
    for method in [m.value for m in methods]:
        tree = method(tree) or tree
    return ElementTree.tostring(tree, encoding='utf-8')
