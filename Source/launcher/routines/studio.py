import launcher.routines.logic as logic
import util.resource
import dataclasses


@dataclasses.dataclass
class _argtype(logic.subparser_argtype):
    cmd_args: list[str] = dataclasses.field(default_factory=list)


class studio(logic.popen_entry):
    local_args: _argtype

    def get_path(self, *paths: str) -> str:
        return util.resource.rōblox_full_path(
            self.global_args.roblox_version,
            'Studio', *paths,
        )

    def get_base_url(self) -> str:
        return \
            f'http{"s" if self.local_args.web_port.is_ssl else""}://' + \
            f'{self.local_args.web_host}:{self.local_args.web_port.port_num}'

    def save_app_setting(self) -> str:
        '''
        Modifies settings to point to correct host name.
        '''
        path = self.get_path('AppSettings.xml')
        with open(path, 'w') as f:
            f.writelines([
                """<?xml version="1.0" encoding="UTF-8"?>""",
                """<Settings>""",
                """\t<ContentFolder>content</ContentFolder>""",
                f"""\t<BaseUrl>{self.get_base_url()}/.</BaseUrl>""",
                """</Settings>""",
            ])
        return path

    def make(self) -> None:
        self.make_popen([
            self.get_path('RobloxStudioBeta.exe'),
            *self.local_args.cmd_args
        ])


class argtype(_argtype):
    obj_type = studio
