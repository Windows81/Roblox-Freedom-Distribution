import re
from . import _logic


def replace(parser: _logic.rbxl_parser, chunk_data: _logic.chunk_data_type) -> bytes | None:
    '''
    Redirects `assetdelivery.roblox.com` links within any `rbxm` data container to `rbxassetid://`.
    '''
    if not isinstance(chunk_data, _logic.chunk_data_type_prop):
        return None

    if chunk_data.prop_type != 0x01:
        return

    prop_values = _logic.split_prop_strings(prop_data)
    results = [
        re.sub(
            br'https?://(?:assetgame\.|assetdelivery\.|www\.)?roblox\.com/(?:v1/)?asset/?\?id=([\d]{1,17})',
            lambda m: b'rbxassetid://%s' % m.group(1),
            v
        )
        for v in prop_values
    ]

    return (
        _logic.get_pre_prop_values_bytes(info) +
        _logic.join_prop_strings(results)
    )
