from . import _logic


def replace(parser: _logic.rbxl_parser, info: _logic.chunk_info) -> bytes | None:
    '''
    Redirects `assetdelivery.roblox.com` links within any `rbxm` data container to your local URL.
    '''
    replacer = _logic.string_replacer(
        br'https?://(?:assetgame\.|assetdelivery\.|www\.)?roblox\.com/(?:v1/)?asset/?\?id=([\d]{1,17})',
        lambda m: b'rbxassetid://%s' % m.group(1),
        info.chunk_data,
    )
    return replacer.calc()
