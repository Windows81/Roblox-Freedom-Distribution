import typing
import enum


class launch_mode(enum.Enum):
    ALWAYS = None
    SERVER = 'server'
    PLAYER = 'player'
    STUDIO = 'studio'


MODE_ALIASES = {
    n: m
    for m in launch_mode
    if m != launch_mode.ALWAYS
    for n in [
        m.value
    ]
    if n != None
}


class callable_list(list[typing.Callable]):
    def call(self, *args, **kwargs) -> list:
        return [
            r
            for f in self
            for r in f(*args, **kwargs) or []
        ]


T = typing.TypeVar('T')


class callable_dict(dict[T, callable_list]):
    def add(self, k: T, *f: typing.Callable):
        self.setdefault(k, callable_list()).extend(f)

    def call(self, k: T, *args, **kwargs) -> list:
        l = self.get(k, None)
        return \
            l.call(*args, **kwargs) \
            if l else []


class mode_dict(callable_dict[launch_mode]):
    def call_auxs(self, mode: launch_mode, *args, **kwargs) -> list:
        return super().call(launch_mode.ALWAYS, mode, *args, **kwargs)

    def call_subparser(self, l_mode: launch_mode, *args, **kwargs) -> list:
        return super().call(l_mode, *args, **kwargs)


ADD_MODE_ARGS = mode_dict()
SERIALISE_ARGS = mode_dict()


def add_args(launch_mode: launch_mode):
    def inner(f):
        ADD_MODE_ARGS.add(launch_mode, f)
        return f
    return inner


def serialise_args(launch_mode: launch_mode):
    def inner(f):
        SERIALISE_ARGS.add(launch_mode, f)
        return f
    return inner
