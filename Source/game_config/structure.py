# pyright: reportAssignmentType=false
# pyright: reportUnknownLambdaType=false

# Local application imports
from config_type.types import structs, wrappers
from config_type.types.callable import obj_type as callable
from . import allocateable
import util.versions
import assets


class config_type(allocateable.obj_type):
    '''
    Configuration specification, according by default to "GameConfig.toml".
    '''
    class metadata(allocateable.obj_type):
        config_version_wildcard: wrappers.rfd_version_check = "*"

    class game_setup(allocateable.obj_type):
        class asset_cache(allocateable.obj_type):
            dir_path: wrappers.path_str = './AssetCache'
            name_template: callable[[int | str], str] = (
                lambda asset_iden: (
                    f'{asset_iden:011d}'
                    if isinstance(asset_iden, int) else
                    asset_iden
                )
            )
            clear_on_start: bool = False

        class persistence(allocateable.obj_type):
            sqlite_path: wrappers.path_str = '_.sqlite'
            clear_on_start: bool = False

        # Don't count too much on 2021E.
        # I really recommend that people manually specify which version of Rōblox they want to run.
        roblox_version: util.versions.rōblox = util.versions.rōblox.v463

    class server_core(allocateable.obj_type):
        class place_file(allocateable.obj_type):
            rbxl_uri: wrappers.uri_obj
            enable_saveplace: bool = False
            track_file_changes: bool = False

        startup_script: str = ''

        class metadata(allocateable.obj_type):
            title: str = 'Untitled'
            description: str = ''
            creator_name: str = 'RFD'
            icon_uri: wrappers.uri_obj | None = None

        chat_style: structs.chat_style = structs.chat_style.CLASSIC_CHAT

        retrieve_default_user_code: callable[[float], str] = (
            lambda tick: 'Player%d' % tick
        )

        check_user_allowed: callable[[int, str], bool] = (
            lambda *a: True
        )

        check_user_has_admin: callable[[int, str], bool] = (
            lambda *a: False
        )

        retrieve_username: callable[[int, str], str] = (
            lambda i, n, *a: n
        )

        retrieve_user_id: callable[[str], int] = wrappers.counter().__call__

        retrieve_avatar: callable[[int, str], structs.avatar_data] = (
            lambda *a: {
                "type": "R15",
                "items": [],
                "scales": {
                    "height": 1,
                    "width": 1,
                    "head": 1,
                    "depth": 1,
                    "proportion": 0,
                    "body_type": 0,
                },
                "colors": {
                    "head": 1,
                    "left_arm": 1,
                    "left_leg": 1,
                    "right_arm": 1,
                    "right_leg": 1,
                    "torso": 1,
                },
            }
        )

        retrieve_groups: callable[[int, str], dict[str, int]] = (
            lambda *a: {}
        )

        retrieve_account_age: callable[[int, str], int] = (
            lambda *a: 0
        )

        retrieve_default_funds: callable[[int, str], int] = (
            lambda *a: 0
        )

        filter_text: callable[[str, int, str], str] = (
            lambda t, *a: t
        )

    class remote_data(allocateable.obj_type):
        gamepasses: structs.gamepasses = []
        dev_products: structs.dev_products = []
        asset_redirects: callable[[int | str], assets.asset_redirect | None] = (
            lambda *a: None
        )
        badges: structs.badges = []
