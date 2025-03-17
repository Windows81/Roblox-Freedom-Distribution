import re
from . import _logic


def replace(parser: _logic.rbxl_parser, info: _logic.chunk_info) -> bytes | None:
    '''
    Redirects `assetdelivery.roblox.com` links within any `rbxm` data container to `rbxassetid://`.
    '''
    prop_data = _logic.get_prop_values_bytes(info)
    if prop_data is None:
        return

    prop_values = _logic.split_prop_values(prop_data)
    results = [
        re.sub(
            br'https?://(?:assetgame\.|assetdelivery\.|www\.)?roblox\.com/(?:v1/)?asset/?\?id=([\d]{1,17})',
            lambda m: b'rbxassetid://%s' % m.group(1),
            v
        )
        for v in prop_values
    ]

    return _logic.join_prop_values(results)
