from . import _logic


def replace(parser: _logic.rbxl_parser, info: _logic.chunk_info):
    '''
    Redirects `assetdelivery.roblox.com` links within any `rbxm` data container to your local URL.
    '''
    replacer = _logic.string_replacer(
        br'https://assetdelivery\.roblox\.com/(v1/asset/?\?id=([0-9]+))',
        lambda m: b'rbxassetid://%s' % m.group(2),
        info.chunk_data,
    )
    return replacer.calc()
