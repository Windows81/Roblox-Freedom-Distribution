import launcher.routines.logic as logic
import launcher.routines.webserver
import dataclasses


@dataclasses.dataclass
class argtype(logic.subparser_argtype):
    cmd_args: list[str] = dataclasses.field(default_factory=list)


class studio(launcher.routines.webserver.webserver_wrap):
    def __init__(self, args: argtype) -> None:
        folder = args.global_args.roblox_version.binary_folder()
        super().__init__([f'{folder}/Studio/RobloxStudioBeta.exe', *args.cmd_args])
