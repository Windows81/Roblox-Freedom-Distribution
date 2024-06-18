import typing_extensions
import enum


class rōblox(enum.Enum):
    # v271 = '2016L'
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
    def from_name(value: str | int):
        return VERSION_MAP[str(value)]


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
