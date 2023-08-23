import util.versions as versions
import dataclasses
import subprocess


class routine(subprocess.Popen):
    @classmethod
    def run(cls, argtype_obj):
        instance = cls(argtype_obj)
        try:
            instance.communicate()
        except KeyboardInterrupt:
            pass
        finally:
            del instance


@dataclasses.dataclass
class global_argtype:
    roblox_version: versions.Version
    parser_class: type[routine]


class subparser_argtype:
    global_args: global_argtype = None
