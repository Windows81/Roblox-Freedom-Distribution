import launcher.routines.logic as logic
import launcher.routines.webserver
import dataclasses


@dataclasses.dataclass
class _argtype(logic.subparser_argtype):
    cmd_args: list[str] = dataclasses.field(default_factory=list)


class studio(logic.popen_entry):
    def __init__(self, global_args: logic.global_argtype, args: _argtype) -> None:
        folder = global_args.roblox_version.binary_full_path('Studio')
        self.make_popen([f'{folder}/RobloxStudioBeta.exe', *args.cmd_args])


class argtype(_argtype):
    obj_type = studio
