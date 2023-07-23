
import launcher.webserver
import launcher.versions


class Studio(launcher.webserver.WebserverWrap):
    def __init__(
        self,
        version: launcher.versions.Version,
        args: list[str] = [],
        **kwargs,
    ) -> None:
        super().__init__([f'{version.folder()}/Studio/RobloxStudioBeta.exe', *args])
