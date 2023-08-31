import launcher.subparsers.aux_tasks._logic
import urllib.request
import util.resource
import util.versions
import util.const
import py7zr
import io


class obj_type(launcher.subparsers.aux_tasks._logic.action):
    def __init__(self, version: util.versions.rōblox, dir_name: str):
        super().__init__()
        self.rōblox_version = version
        self.dir_name = dir_name

    def retrieve_version(self) -> util.versions.rōblox:
        return self.local_args.rōblox_version

    def get_link(self) -> str:
        return \
            'https://github.com/Windows81/Roblox-Filtering-Disabled/releases/download/' + \
            f'{util.const.GIT_RELEASE_VERSION}/{self.rōblox_version.name}.{self.dir_name}.7z'

    def initialise(self) -> None:
        res = urllib.request.urlopen(self.get_link()).read()
        full_dir = util.resource.retr_rōblox_full_path(self.rōblox_version, self.dir_name)
        py7zr.unpack_7zarchive(io.BytesIO(res), full_dir)
