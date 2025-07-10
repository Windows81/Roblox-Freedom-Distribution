# pyright: reportImportCycles=false
# TODO: simplify import heirarchy

# Standard library imports
from typing import Callable
import dataclasses
import functools
import os
import shutil

# Internal or local application imports
import util.const
from . import material, queue, returns, serialisers, extractor


@dataclasses.dataclass
class asset_redirect:
    def __post_init__(self) -> None:
        if sum([
            self.cmd_line is not None,
            self.raw_data is not None,
            self.forward_url is not None,
        ]) > 1:
            raise Exception(
                'Entries for `asset_redirects` should not have ' +
                'more than one of a `forward_url`, a pipeable `cmd_line`, or a `raw_data` chunk.'
            )
    forward_url: str | None = None
    raw_data: bytes | None = None
    cmd_line: str | None = None


class asseter:
    def __init__(
        self,
        dir_path: str,
        redirect_func: Callable[[int | str], asset_redirect | None],
        asset_name_func: Callable[[int | str], str],
        clear_on_start: bool,
    ) -> None:
        super().__init__()
        self.dir_path = dir_path
        self.redirect_func = redirect_func
        self.asset_name_func = asset_name_func
        self.queuer = queue.queuer()

        if os.path.isdir(dir_path):
            if clear_on_start:
                shutil.rmtree(dir_path)
                os.makedirs(dir_path)
        else:
            os.makedirs(dir_path)

    @functools.cache
    def get_asset_path(self, asset_id: int | str) -> str:
        return os.path.normpath(
            os.path.join(
                self.dir_path,
                self.asset_name_func(asset_id),
            )
        )

    def _load_file(self, path: str) -> bytes | None:
        if not os.path.isfile(path):
            return None

        with open(path, 'rb') as f:
            return f.read()

    def _save_file(self, path: str, data: bytes) -> None:
        try:
            with open(path, 'wb') as f:
                f.write(data)
        except OSError:  # Might occur when the asset iden is too long.
            pass

    def _load_online_asset(self, asset_id: int) -> bytes | None:
        data = self.queuer.get(asset_id, extractor.download_rōblox_asset)
        if data is None:
            return None

        data = serialisers.parse(data)
        return data

    def resolve_asset_id(self, id_str: str | None) -> int | None:
        if id_str is None:
            return None
        try:
            return int(id_str)
        except ValueError:
            return None

    def resolve_asset_version_id(self, id_str: str | None) -> int | None:
        # Don't assume this is true for Rōblox.com:
        # RFD treats 'asset version idens' the same way as just plain 'version idens'.
        return self.resolve_asset_id(id_str)

    def resolve_asset_query(self, query: dict[str, str]) -> int | str | None:
        candidate_funcs = [
            (query.get('id'), self.resolve_asset_id),
            (query.get('assetversionid'), self.resolve_asset_version_id),
        ]

        for (prop_val, func) in candidate_funcs:
            if prop_val is None:
                continue
            result = func(prop_val)
            if result is not None:
                return result
        for (prop_val, func) in candidate_funcs:
            if prop_val is not None:
                return prop_val

    def add_asset(self, asset_id: int | str, data: bytes) -> None:
        path = self.get_asset_path(asset_id)
        self._save_file(path, data)

    @functools.cache
    def is_blocklisted(self, asset_id: int | str) -> bool:
        '''
        This is to make sure that unauthorised clients can't get private (i.e., place map) files.
        '''
        asset_path = self.get_asset_path(asset_id)
        place_path = self.get_asset_path(util.const.PLACE_IDEN_CONST)
        if asset_path == place_path:
            return True
        return False

    def _load_asset_num(self, asset_id: int) -> bytes | None:
        return self._load_online_asset(asset_id)

    def _load_asset_str(self, asset_id: str) -> bytes | None:
        if asset_id.startswith(material.const.ID_PREFIX):
            return material.load_asset(asset_id)
        return None

    def _load_redir_asset(self, asset_id: int | str, redirect: asset_redirect) -> returns.base_type:
        asset_path = self.get_asset_path(asset_id)
        local_data = self._load_file(asset_path)
        if local_data is not None:
            return returns.construct(data=local_data)

        if redirect.forward_url is not None:
            return returns.construct(
                redirect_url=redirect.forward_url,
            )
        elif redirect.cmd_line is not None:
            # NOTE: redirect asset ids which share the same command line may also share the same output dump.
            # This happens when both assets are loaded near the same time.
            return returns.construct(
                data=self.queuer.get(
                    redirect.cmd_line,
                    extractor.process_command_line,
                ),
            )
        elif redirect.raw_data is not None:
            return returns.construct(
                data=redirect.raw_data,
            )
        else:
            return returns.construct()

    def _load_asset(self, asset_id: int | str) -> returns.base_type:
        redirect_info = self.redirect_func(asset_id)
        if redirect_info is not None:
            return self._load_redir_asset(asset_id, redirect_info)

        asset_path = self.get_asset_path(asset_id)
        local_data = self._load_file(asset_path)
        if local_data is not None:
            return returns.construct(data=local_data)

        if isinstance(asset_id, str):
            return returns.construct(data=self._load_asset_str(asset_id))
        else:
            return returns.construct(data=self._load_asset_num(asset_id))

    def get_asset(
        self,
        asset_id: int | str,
        bypass_blocklist: bool = False
    ) -> returns.base_type:
        if not bypass_blocklist and self.is_blocklisted(asset_id):
            returns.construct(error='Asset is blocklisted.')

        asset_path = self.get_asset_path(asset_id)
        result_data = self._load_asset(asset_id)

        if isinstance(result_data, returns.ret_data):
            self._save_file(asset_path, result_data.data)
        return result_data
