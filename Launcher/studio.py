import versions
import uwamp


class Studio(uwamp.UwAmpWrap):
    def __init__(self, version: versions.Version, **kwargs) -> None:
        super().__init__(f'{version.folder()}/Studio/RobloxStudioBeta.exe', **kwargs)
