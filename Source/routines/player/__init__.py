# Standard library imports
import functools
import json
import urllib.error
import urllib.parse
import urllib.request
import dataclasses
import ipaddress
import time

# Typing imports
from typing import ClassVar, override

# Local application imports
from .. import _logic as logic
import util.player_cookie_store
import util.resource
import util.versions
import util.const


@dataclasses.dataclass(kw_only=True, unsafe_hash=True)
class obj_type(logic.bin_entry):
    BIN_SUBTYPE: ClassVar = util.resource.bin_subtype.PLAYER
    DIRS_TO_ADD: ClassVar = ['logs', 'LocalStorage']

    web_host: str = 'localhost'
    web_port: int = util.const.RFD_DEFAULT_PORT
    rcc_host: str | None
    rcc_port: int | None
    app_host: str = dataclasses.field(init=False)

    user_code: str | None
    launch_delay: float = 0

    @override
    def __post_init__(self) -> None:
        super().__post_init__()
        (
            self.web_host, self.rcc_host,
        ) = self.maybe_differenciate_web_and_rcc_stuff(
            self.web_host, self.rcc_host,
        )
        (
            self.web_port, self.rcc_port,
        ) = self.maybe_differenciate_web_and_rcc_stuff(
            self.web_port, self.rcc_port,
        )
        (
            self.rcc_host, self.rcc_port,
        ) = self.maybe_separate_host_and_port(
            self.rcc_host, self.rcc_port,
        )

        if self.rcc_host == 'localhost':
            self.rcc_host = '127.0.0.1'

        self.app_host = self.web_host
        if self.web_host == 'localhost':
            self.web_host = self.app_host = '127.0.0.1'

        elif self.app_host.startswith('['):
            # Converts
            # - "[2607:fb91:1b74:d4d8:3dfb:5a51:55c3:d516]" into
            # - "[2607:fb91:1b74:d4d8:3dfb:5a51:85.195.213.22]"
            # This is because Rōblox's CoreScripts do not like working with `BaseUrl` settings which don't have dots.
            prefix_len = 30
            ipv6_obj = ipaddress.IPv6Address(self.web_host[1:-1])
            ipv4_mapped = ipaddress.IPv4Address(int(ipv6_obj) & 0xFFFFFFFF)
            exploded_str = ipv6_obj.exploded
            self.app_host = f"[{exploded_str[:prefix_len]}{ipv4_mapped!s}]"

    def finalise_user_code(self) -> None:
        '''
        This method is separate from `__post_init__` because
        it needs to be executed after `launch_delay` seconds.
        The `__post_init__` method gets executed before that delay.
        '''
        if self.user_code is not None:
            return
        res = self.send_request('/rfd/default-user-code')
        self.user_code = str(res.read(), encoding='utf-8')

    def get_auth_cookie(self) -> str | None:
        return util.player_cookie_store.get_cookie_value(
            preferred_hosts={
                self.web_host,
                self.app_host,
                'localhost',
                '127.0.0.1',
            },
        )

    def get_cookie_join_data(
        self,
        cookie: str | None = None,
        *,
        attempts: int = 10,
        retry_delay: float = 1,
    ) -> dict[str, str] | None:
        cookie = cookie or self.get_auth_cookie()
        if cookie is None:
            return None

        query = urllib.parse.urlencode({
            k: v for k, v in {
                'placeId': util.const.PLACE_IDEN_CONST,
                'MachineAddress': self.rcc_host,
                'ServerPort': self.rcc_port,
            }.items() if v is not None
        })
        request = urllib.request.Request(
            url=f'{self.get_base_url()}/game/get-join-script?{query}',
            headers={
                'Cookie': f'.ROBLOSECURITY={cookie}',
                'X-Roblosecurity': cookie,
            },
        )
        last_error: Exception | None = None
        for attempt in range(attempts):
            try:
                response = urllib.request.urlopen(
                    request,
                    context=self.get_none_ssl(),
                    timeout=7,
                )
                with response:
                    payload = json.loads(str(response.read(), encoding='utf-8'))
                if not isinstance(payload, dict):
                    raise ValueError('Join payload is not a JSON object')

                join_script_url = payload.get('joinScriptUrl')
                authentication_url = payload.get('authenticationUrl')
                if not isinstance(join_script_url, str):
                    raise ValueError('joinScriptUrl is missing')
                if not isinstance(authentication_url, str):
                    raise ValueError('authenticationUrl is missing')
                return payload
            except urllib.error.HTTPError as exc:
                last_error = exc
                if exc.code in {400, 401, 403}:
                    break
                if attempt + 1 >= attempts:
                    break
                time.sleep(retry_delay)
            except Exception as exc:
                last_error = exc
                if attempt + 1 >= attempts:
                    break
                time.sleep(retry_delay)

        if last_error is not None:
            self.log(
                'Authenticated player launch failed: %s' %
                (last_error,)
            )
        return None

    @override
    def get_base_url(self) -> str:
        return f'https://{self.web_host}:{self.web_port}'

    @override
    def get_app_base_url(self) -> str:
        return f'https://{self.app_host}:{self.web_port}'

    @override
    @functools.cache
    def retr_version(self) -> util.versions.rōblox:
        res = self.send_request('/rfd/roblox-version')
        return util.versions.rōblox.from_name(
            str(res.read(), encoding='utf-8'),
        )

    @override
    def bootstrap(self) -> None:
        super().bootstrap()
        time.sleep(self.launch_delay)
        self.finalise_user_code()
        self.make_client_popen()

    def build_place_launcher_url(
        self,
        *,
        include_user_code: bool,
    ) -> str:
        base_url = self.get_base_url()
        query_data = {
            'MachineAddress': self.rcc_host,
            'ServerPort': self.rcc_port,
        }
        if include_user_code:
            query_data |= {
                'UserCode': self.user_code,

                # Temporary backwards compatibility below 0.65.1.
                # Might get rid of in six or seven months.
                'rcc-host-addr': self.rcc_host,
                'rcc-port': self.rcc_port,
                'user-code': self.user_code,
            }

        return (
            f'{base_url}/game/PlaceLauncher.ashx?' +
            urllib.parse.urlencode({
                key: value
                for key, value in query_data.items()
                if value is not None
            })
        )

    def make_client_popen(self) -> None:
        base_url = self.get_base_url()
        auth_cookie = self.get_auth_cookie()
        join_data = self.get_cookie_join_data(auth_cookie)
        if join_data is not None:
            join_script_url = str(join_data['joinScriptUrl'])
            authentication_url = str(join_data['authenticationUrl'])
        else:
            if auth_cookie is None:
                self.log(
                    'Launching player without auth cookie; '
                    'client will handle the auth error.'
                )
            else:
                self.log(
                    'Launching player without authenticated join data; '
                    'client will handle the auth error.'
                )
            join_script_url = self.build_place_launcher_url(
                include_user_code=False,
            )
            authentication_url = f'{base_url}/login/negotiate.ashx'

        self.init_popen(
            self.get_versioned_path('RobloxPlayerBeta.exe'),
            (
                '-a', authentication_url,
                '-j', join_script_url,
                '-t', '1',
            ))

    @override
    def restart(self) -> None:
        self.stop()
        self.bootstrap()
        self.make_client_popen()
