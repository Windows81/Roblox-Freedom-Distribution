import enum


class Version(enum.Enum):
    v348 = '2018M'
    v547 = '2022L'

    def binary_folder(self) -> str:
        return f'./Roblox/{self.name}'

    def get_number(self) -> int:
        return int(self.name[1:])

    def security_versions(self) -> list[str]:
        num = self.get_number()
        return [
            f"0.{num}.0pcplayer",
            f"2.{num}.0androidapp",
        ]


VERSION_MAP = dict(
    (k, e)
    for e in Version
    for k in
    [
        e.value,
        e.name[1:],
    ]
)

VERSION_ROUTINES = {
    Version.v348: [],
    Version.v547: [],
}
