from functools import partial
import enum

from . import (
    rbxl,
    mesh,
)


class method(enum.Enum):
    # Why `partial`?
    # https://stackoverflow.com/a/58714331/6879778
    rbxl = enum.member(partial(rbxl.parse))
    mesh = enum.member(partial(mesh.parse))


def parse(data: bytes, items: set[method] = set(method)) -> bytes:
    for m in items:
        data = m.value(data)
    return data
