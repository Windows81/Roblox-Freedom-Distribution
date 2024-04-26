import launcher.routines._logic as logic
import launcher.aux_tasks.download
import util.resource
import util.versions
import dataclasses
import util.const


@dataclasses.dataclass
class _arg_type(logic.arg_type):
    rōblox_version: util.versions.rōblox
    dir_name: str


class obj_type(logic.bin_entry):
    local_args: _arg_type

    def initialise(self) -> None:
        launcher.aux_tasks.download.obj_type(
            rōblox_version=self.local_args.rōblox_version,
            dir_name=self.local_args.dir_name,
        )


class arg_type(_arg_type):
    obj_type = obj_type
