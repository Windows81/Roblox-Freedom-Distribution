from functools import partial
import enum

from . import (
    rbxl,
    mesh,
    video,
)


class method(enum.Enum):
    # Why `partial`?
    # https://stackoverflow.com/a/58714331/6879778
    rbxl = enum.member(partial(rbxl.parse))
    mesh = enum.member(partial(mesh.parse))
    video = enum.member(partial(video.parse))


ALL_METHODS = set(method)


def parse(data: bytes, items: set[method] = ALL_METHODS) -> bytes:
    for m in items:
        result = m.value(data)
        if result is not None:
            return result
    return data
