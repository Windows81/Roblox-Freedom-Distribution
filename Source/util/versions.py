import typing
import enum


class rōblox(enum.Enum):
    v348 = '2018M'
    v463 = '2021E'
    v547 = '2022L'

    def get_number(self) -> int:
        return int(self.name[1:])

    def security_versions(self) -> list[str]:
        num = self.get_number()
        return [
            f"0.{num}.0pcplayer",
            f"2.{num}.0androidapp",
        ]

    @staticmethod
    def from_name(value: str | int):
        return VERSION_MAP[str(value)]


VERSION_MAP = dict(
    (k, e)
    for e in rōblox
    for k in
    [
        e.name,
        e.value,
        e.name[1:],
    ]
)


T = typing.TypeVar('T')


class version_holder(dict[rōblox, T]):
    def __add_pred(self, func: typing.Callable[[int], bool], obj: T) -> T:
        for v in rōblox:
            if not func(v.get_number()):
                continue
            super().__setitem__(v, obj)
        return obj

    def add_min(self, obj: T, min_version: int) -> T:
        return self.__add_pred(lambda n: n >= min_version, obj)

    def add_all(self, obj: T) -> T:
        return self.__add_pred(lambda n: True, obj)
