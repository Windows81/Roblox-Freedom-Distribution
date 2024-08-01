from . import cache


class asseter:
    def __init__(self, dir_path: str, clear_on_start: bool = False) -> None:
        self.cache = cache.cacher(
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

    def load_asset(self, asset_id) -> bytes | None:
        if isinstance(asset_id, str):
            return self.cache.load_asset_str(asset_id)
        elif isinstance(asset_id, int):
            return self.cache.load_asset_num(asset_id)
