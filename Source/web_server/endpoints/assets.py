from web_server._logic import web_server_handler, server_path
import assets.returns as returns
import util.const


@server_path("/asset")
@server_path("/asset/")
@server_path("/v1/asset")
@server_path("/v1/asset/")
@server_path("/.127.0.0.1/asset/")
def _(self: web_server_handler) -> bool:
    asset_cache = self.server.game_data.asset_cache

    # Paramater can either be `id` or `assetversionid`.
    asset_id = asset_cache.resolve_asset_query(self.query)

    # TODO: use a proper allow-listing system.
    # RFD is designed to allow you to run a webserver separately from RCC.
    # This limitation breaks that design.
    is_priviledged = self.domain == 'localhost'

    if (
        asset_id == util.const.PLACE_IDEN_CONST and
        not is_priviledged
    ):
        self.send_error(
            403,
            "Server hosters don't tend to like exposing their place files.  " +
            "Ask them if they'd be willing to lend this one to you.",
        )
        return True

    asset = asset_cache.get_asset(
        asset_id,
        bypass_blacklist=is_priviledged,
    )

    if isinstance(asset, returns.ret_data):
        self.send_data(asset.data)
        return True
    elif isinstance(asset, returns.ret_none):
        self.send_error(404)
        return True
    elif isinstance(asset, returns.ret_relocate):
        self.send_redirect(asset.url)
        return True
    return False


@server_path('/ownership/hasasset', commands={'GET'})
def _(self: web_server_handler) -> bool:
    '''
    Typically used to check if players own specific catalogue items.
    There are no current plans to implement catalogue APIs in RFD.
    Collective ownership it is...
    '''
    self.send_json('true')
    return True
