import web_server._logic as web_server
from . import _logic as logic
import util.resource
import dataclasses
import os


class obj_type(logic.bin_entry):
    local_args: 'arg_type'
    BIN_SUBTYPE = util.resource.bin_subtype.STUDIO

    def save_app_setting(self) -> str:
        '''
        Modifies settings to point to correct host name.
        '''
        path = self.get_versioned_path('AppSettings.xml')
        with open(path, 'w', encoding='utf-8') as f:
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
            self.get_versioned_path('RobloxStudioBeta.exe'),
            *self.local_args.cmd_args
        ])


@dataclasses.dataclass
class arg_type(logic.bin_arg_type):
    obj_type = obj_type

    cmd_args: list[str] = dataclasses.field(default_factory=list)
    web_host: str | None = None
    web_port: web_server.port_typ = \
        web_server.port_typ(
            port_num=80,
            is_ssl=False,
            is_ipv6=False,
        ),  # type: ignore

    def get_base_url(self) -> str:
        return \
            f'http{"s" if self.web_port.is_ssl else ""}://' + \
            f'{self.web_host}:{self.web_port.port_num}'
