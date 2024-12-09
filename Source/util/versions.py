import typing
import functools
import enum


@functools.total_ordering
class rōblox(enum.Enum):
    # v271 = ('2016L', '2016',)
    v348 = ('2018M', '2018',)
    v463 = ('2021E', '2021',)

    # TODO: get 2022L Studio to work with this program.
    # v547 = '2022L'

    def get_number(self) -> int:
        return int(self.name[1:])

    def security_versions(self) -> list[str]:
        num = self.get_number()
        return [
            f"0.{num}.0pcplayer",
            f"2.{num}.0androidapp",
        ]

    @staticmethod
    def from_name(value: int | str) -> "rōblox":
        return VERSION_MAP[str(value)]

    def __lt__(self, other: typing.Self) -> bool:
        return self.get_number() < other.get_number()


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
