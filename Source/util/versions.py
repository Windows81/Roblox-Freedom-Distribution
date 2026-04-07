import functools
import typing
import enum


@functools.total_ordering
class rōblox(enum.Enum):
    v347 = ('2018M', '2018', 'v348',)
    v463 = ('2021E', '2021',)

    def get_number(self) -> int:
        return int(self.name[1:])

    @staticmethod
    def from_name(value: int | str) -> "rōblox":
        return VERSION_MAP[str(value)]

    def __lt__(self, other: typing.Self) -> bool:
        return self.get_number() < other.get_number()

    @classmethod
    def get_all_versions(cls) -> set[typing.Self]:
        return set(cls)


FIRST_VERSION = min(rōblox)
LAST_VERSION = max(rōblox)


VERSION_MAP = dict(
    (k, e)
    for e in rōblox
    for k in
    [
        e.name,
        *e.value,
        e.name[1:],
    ]
)
