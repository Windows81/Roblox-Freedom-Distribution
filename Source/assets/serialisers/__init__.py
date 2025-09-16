from functools import partial
import enum

from . import (
    rbxl,
    rbxlx,
    mesh,
    video,
    csg,
)


class method(enum.Enum):
    # Why `partial`?
    # https://stackoverflow.com/a/58714331/6879778
    rbxl = enum.member(partial(rbxl.parse))
    rbxlx = enum.member(partial(rbxlx.parse))
    mesh = enum.member(partial(mesh.parse))
    csg = enum.member(partial(csg.parse))
    video = enum.member(partial(video.parse))


ALL_METHODS = set(method)


def parse(data: bytes, methods: set[method] = ALL_METHODS) -> tuple[bytes, bool]:
    for m in methods:
        result = m.value(data)
        if result is not None:
            return (result, True)
    return (data, False)
