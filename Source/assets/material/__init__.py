from .. import extract
from . import const
import urllib3


def transform_to_id_num(asset_id: str) -> int:
    asset_sub = asset_id[len(const.ID_PREFIX):]

    result = const.MATERIAL_DICT_2022.get(asset_sub, 153465633)
    return result


def split_asset_str(asset_id: str) -> None | tuple[str, ...]:
    asset_sub = asset_id[len(const.ID_PREFIX):]

    # Example: `wood-diffuse.dds`
    sub_pieces = asset_sub.lower().split('-')
    if len(sub_pieces) != 2:
        return None

    extension_index = sub_pieces[-1].rfind('.')
    return (
        *sub_pieces[:-1],
        sub_pieces[-1][:extension_index],
        sub_pieces[-1][extension_index:],
    )


def load_asset(asset_id: str) -> bytes | None:

    # Example: `wood`, `diffuse`, `.dds`.
    # Reconstructs as `wood-diffuse.dds`.
    sub_pieces = split_asset_str(asset_id)
    if sub_pieces is None:
        return None
    piece_combos = [sub_pieces]

    # Adds `reflection` as a backup for `specular` textures.
    # This is to ensure better compatibility with versions older than 2021E.
    if sub_pieces[1] == 'specular':
        piece_combos += [
            (*combo[:1], 'reflection', *combo[2:],)
            for combo in piece_combos
        ]

    # TODO: make material URL scheme more flexible.
    for combo in piece_combos:
        url = (
            # 'https://github.com/Windows81/Roblox-Materials/raw/main/textures/Extrapolated2022/'
            'https://github.com/Windows81/Roblox-Materials/raw/main/textures/ExperiencersInternational2021/%s%s' %
            ('/'.join(combo[:-1]), combo[-1])
        )

        http = urllib3.PoolManager()
        response = http.request('GET', url)
        if response.status == 200:
            return response.data

    id_num = transform_to_id_num(asset_id)
    return extract.download_rōblox_asset(id_num)
