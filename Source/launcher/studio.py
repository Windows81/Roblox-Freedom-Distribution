
import launcher.webserver
import versions


class Studio(launcher.webserver.WebserverWrap):
    def __init__(
        self,
        version: versions.Version,
        args: list[str] = [],
        **kwargs,
    ) -> None:
        super().__init__([f'{version.binary_folder()}/Studio/RobloxStudioBeta.exe', *args])
