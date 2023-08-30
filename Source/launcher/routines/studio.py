import launcher.routines._logic as sub_logic
import dataclasses


@dataclasses.dataclass
class _arg_type(sub_logic.arg_type):
    cmd_args: list[str] = dataclasses.field(default_factory=list)


class obj_type(sub_logic.bin_entry):
    local_args: _arg_type
    DIR_NAME = 'Studio'

    def get_base_url(self) -> str:
        return \
            f'http{"s" if self.local_args.web_port.is_ssl else""}://' + \
            f'{self.local_args.web_host}:{self.local_args.web_port.port_num}'

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
                f"""\t<BaseUrl>{self.get_base_url()}/.</BaseUrl>""",
                """</Settings>""",
            ])
        return path

    def initialise(self) -> None:
        self.make_popen([
            self.get_versioned_path('RobloxStudioBeta.exe'),
            *self.local_args.cmd_args
        ])


class arg_type(_arg_type):
    obj_type = obj_type
