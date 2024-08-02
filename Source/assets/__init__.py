from util.types import structs, wrappers
from . import extract, returns


class asseter:
    def __init__(
        self,
        dir_path: str,
        redirects: structs.asset_redirects,
        clear_on_start: bool,
    ) -> None:
        self.redirects = redirects
        self.cache = extract.extractor(
            dir_path=dir_path,
            clear_on_start=clear_on_start,
        )

    def resolve_asset_id(self, id_str: str | None) -> int | None:
        if id_str is None:
            return None
        try:
            return int(id_str)
        except ValueError:
            return None

    def resolve_asset_version_id(self, id_str: str | None) -> int | None:
        # Don't assume this is true for production Rōblox:
        # RFD treats 'asset version ids' the same way as just plain 'version ids'.
        return self.resolve_asset_id(id_str)

    def resolve_asset_query(self, query: dict[str, str]) -> int | str:
        funcs = [
            (query.get('id'), self.resolve_asset_id),
            (query.get('assetversionid'), self.resolve_asset_version_id),
        ]

        for (prop_val, func) in funcs:
            if prop_val is None:
                continue
            result = func(prop_val)
            if result is not None:
                return result
        for (prop_val, func) in funcs:
            if prop_val is not None:
                return prop_val
        raise ValueError()

    def redirect_asset(self, redir_uri: wrappers.uri_obj) -> returns.base_type:
        if redir_uri.is_online:
            return returns.construct(redirect_url=redir_uri.value)
        with open(redir_uri.value, 'rb') as f:
            return returns.construct(data=f.read())

    def get_asset(self, asset_id: int | str, bypass_blacklist: bool = False) -> returns.base_type:
        redirect = self.redirects.get(asset_id)
        if redirect is not None:
            return self.redirect_asset(redirect.uri)
        return returns.construct(data=self.cache.load_asset(asset_id, bypass_blacklist))

    def add_asset(self, asset_id: int | str, data: bytes) -> None:
        redirect = self.redirects.get(asset_id)
        if redirect is not None:
            raise FileExistsError()
        self.cache.save_asset(asset_id, data)
