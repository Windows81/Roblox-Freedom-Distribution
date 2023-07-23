import enum


class Version(enum.Enum):
    v2018M = '2018M'
    v2022L = '2022L'

    def folder(self):
        return f'./Roblox/{self.value}'


VERSION_MAP = {e.name: e for e in Version} | {e.value: e for e in Version}

VERSION_ROUTINES = {
    Version.v2018M: [],
    Version.v2022L: [],
}
