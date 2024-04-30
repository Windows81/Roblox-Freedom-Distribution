import launcher.routines._logic as logic
import dataclasses
import os


@dataclasses.dataclass
class _arg_type(logic.bin_arg_type):
    cmd_args: list[str] = dataclasses.field(default_factory=list)
    web_host: str | None = None
    web_port: logic.port = \
        logic.port(
            port_num=80,
            is_ssl=False,
            is_ipv6=False,
        ),  # type: ignore

    def get_base_url(self) -> str:
        return \
            f'http{"s" if self.web_port.is_ssl else ""}://' + \
            f'{self.web_host}:{self.web_port.port_num}'


class obj_type(logic.bin_entry):
    local_args: _arg_type
    DIR_NAME = 'Studio'

    def save_app_setting(self) -> str:
        '''
        Modifies settings to point to correct host name.
        '''
        path = self.get_versioned_path('AppSettings.xml')
        with open(path, 'w') as f:
            f.writelines([
                """<?xml version="1.0" encoding="UTF-8"?>""",
                """<Settings>""",
                """\t<ContentFolder>content</ContentFolder>""",
                f"""\t<BaseUrl>{self.local_args.get_base_url()}/.</BaseUrl>""",
                """</Settings>""",
            ])
        return path

    def process(self) -> None:
        self.make_popen([
            *(() if os.name == 'nt' else ('wine',)),
            self.get_versioned_path('RobloxStudioBeta.exe'),
            *self.local_args.cmd_args
        ])


class arg_type(_arg_type):
    obj_type = obj_type
