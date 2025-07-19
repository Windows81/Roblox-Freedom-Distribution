import re
from . import _logic


def replace(parser: _logic.rbxl_parser, chunk_data: _logic.chunk_data_type) -> _logic.chunk_data_type | None:
    '''
    Redirects `assetdelivery.roblox.com` links within any `rbxm` data container to `rbxassetid://`.
    '''
    if not isinstance(chunk_data, _logic.chunk_data_type_prop):
        return None

    if chunk_data.prop_type != 0x01:
        return

    chunk_data.prop_values = _logic.join_prop_strings([
        re.sub(
            br'https?://(?:assetgame\.|assetdelivery\.|www\.)?roblox\.com/(?:v1/)?asset/?\?id=([\d]{1,17})',
            lambda m: b'rbxassetid://%s' % m.group(1),
            v
        )
        for v in _logic.split_prop_strings(chunk_data.prop_values)
    ])

    return chunk_data
