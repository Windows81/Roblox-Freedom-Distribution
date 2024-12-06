from config_type.types.callable import obj_type as callable
from config_type.types import structs, wrappers
from . import allocateable
import util.versions
import util.resource
import textwrap


class config_type(allocateable.obj_type):
    '''
    Configuration specification, according by default to "GameConfig.toml".
    '''
    class metadata(allocateable.obj_type):
        config_version_wildcard: wrappers.rfd_version_check = "*"  # type:ignore

    class game_setup(allocateable.obj_type):
        class asset_cache(allocateable.obj_type):
            dir_path: wrappers.path_str = './AssetCache'  # type:ignore
            clear_on_start: bool = False

        class persistence(allocateable.obj_type):
            sqlite_path: wrappers.path_str = '_.sqlite'  # type:ignore
            clear_on_start: bool = False

        roblox_version: util.versions.rōblox

    class server_core(allocateable.obj_type):
        class place_file(allocateable.obj_type):
            rbxl_uri: wrappers.uri_obj
            enable_saveplace: bool = False

        startup_script: str = ''

        class metadata(allocateable.obj_type):
            title: str = 'Untitled'
            description: str = ''
            creator_name: str = 'RFD'
            icon_uri: wrappers.uri_obj = ''  # type:ignore

        chat_style: structs.chat_style = structs.chat_style.CLASSIC_CHAT

        retrieve_default_user_code: callable[[float], str] = textwrap.dedent('''\
        def f(tick):
            return 'Player%d' % tick
        ''')  # type: ignore

        check_user_allowed: callable[[int, str], bool] = textwrap.dedent('''\
        def f(*a):
            return True
        ''')  # type: ignore

        check_user_has_admin: callable[[int, str], bool] = textwrap.dedent('''\
        def f(*a):
            return False
        ''')  # type: ignore

        retrieve_username: callable[[int, str], str] = textwrap.dedent('''\
        def f(i, n, *a):
            return n
        ''')  # type: ignore

        retrieve_user_id: callable[[str], int] = textwrap.dedent('''\
        count = 0
        def f(*a):
            nonlocal count
            count += 1
            return count
        ''')  # type: ignore

        retrieve_avatar_type: callable[[int, str], structs.avatar_type] = textwrap.dedent('''\
        def f():
            return 'R6'
        ''')  # type: ignore

        retrieve_avatar_items: callable[[int, str], list[int]] = textwrap.dedent('''\
        def f():
            return []
        ''')  # type: ignore

        retrieve_avatar_scales: callable[[int, str], structs.avatar_scales] = textwrap.dedent('''\
        def f():
            return {
                "height": 1,
                "width": 1,
                "head": 1,
                "depth": 1,
                "proportion": 0,
                "body_type": 0,
            }
        ''')  # type: ignore

        retrieve_avatar_colors: callable[[int, str], structs.avatar_colors] = textwrap.dedent('''\
        def f():
            return {
                "head": 1,
                "left_arm": 1,
                "left_leg": 1,
                "right_arm": 1,
                "right_leg": 1,
                "torso": 1,
            }
        ''')  # type: ignore

        retrieve_groups: callable[[int, str], dict[str, int]] = textwrap.dedent('''\
        def f(*a):
            return []
        ''')  # type: ignore

        retrieve_account_age: callable[[int, str], int] = textwrap.dedent('''\
        def f(*a):
            return 0
        ''')  # type: ignore

        retrieve_default_funds: callable[[int, str], int] = textwrap.dedent('''\
        def f(*a):
            return 0
        ''')  # type: ignore

        filter_text: callable[[str, int, str], str] = textwrap.dedent('''\
        def f(t, *a):
            return t
        ''')  # type: ignore

    class remote_data(allocateable.obj_type):
        gamepasses: structs.gamepasses = []  # type: ignore
        asset_redirects: callable[[int | str], structs.asset_redirect | None] = textwrap.dedent('''\
        def f(*a):
            return None
        ''')  # type: ignore
        badges: structs.badges = []  # type: ignore
