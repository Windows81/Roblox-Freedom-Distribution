from web_server._logic import web_server_handler, server_path
import util.versions as versions
import re


@server_path('/Game/GamePass/GamePassHandler.ashx', commands={'GET'})
def _(self: web_server_handler) -> bool:
    '''
    TODO: handle social requests.
    '''
    match self.query['Action']:
        case 'HasPass':
            def check() -> bool:
                gamepass_id = int(self.query['PassID'])
                user_id = int(self.query['UserID'])
                return self.server.storage.gamepasses.check(user_id, gamepass_id) is not None

            self.send_data(bytes(
                '<Value Type="boolean">' +
                ("true" if check() else "false") +
                '</Value>',
                encoding='utf-8',
            ))
            return True

    self.send_json({})
    return True


@server_path('/marketplace/game-pass-product-info', commands={'GET'}, versions={versions.rōblox.v348})
def _(self: web_server_handler) -> bool:
    '''
    https://github.com/InnitGroup/syntaxsource/blob/71ca82651707ad88fb717f3cc5e106ff62ac3013/syntaxwebsite/app/routes/marketplace.py#L21
    '''
    gamepass_id = int(self.query['gamePassId'])
    gamepasses = self.game_config.remote_data.gamepasses
    gamepass = gamepasses.get(gamepass_id)
    if gamepass is None:
        self.send_error(404)
        return True

    self.send_json({
        "AssetId": gamepass.id_num,
        "ProductId": gamepass.id_num,
        "Name": gamepass.name,
        "Description": gamepass.name,
        "Creator": 1,
        "IconImageAssetId": 0,
        "Created": 0,
        "Updated": 0,
        "PriceInRobux": 0,
        "PriceInTickets": 0,
        "Sales": 0,
        "IsNew": False,
        "IsForSale": True,
        "IsPublicDomain": False,
        "IsLimited": False,
        "IsLimitedUnique": False,
        "Remaining": False,
        "MinimumMembershipLevel": 0,
        "ContentRatingTypeId": 0,
    })
    return True


@server_path(r'/v1/users/(\d+)/items/gamepass/(\d+)', regex=True, commands={'GET'})
def _(self: web_server_handler, match: re.Match[str]) -> bool:
    '''
    https://github.com/SushiDesigner/Meteor-back/blob/dc561b5af196ca9c375530d30d593fc8d7f0486c/routes/marketplace.js#L129
    '''
    user_iden = int(match.group(1))
    gamepass_iden = int(match.group(2))
    gamepasses = self.game_config.remote_data.gamepasses

    has_gamepass = self.server.storage.gamepasses.check(
        user_iden,
        gamepass_iden,
    )

    if has_gamepass:
        data = [
            {
                "type": "GamePass",
                "id": gamepass_iden,
                "name": gamepasses.get(gamepass_iden),
                "instanceId": None,
            }
        ]
    else:
        data = []

    self.send_json({
        "previousPageCursor": None,
        "nextPageCursor": None,
        "data": data,
    })
    return True


@server_path('/gametransactions/getpendingtransactions/', commands={'GET'})
def _(self: web_server_handler) -> bool:
    '''
    Something to do with developer products.
    Won't be implemented in RFD right now.
    https://github.com/InnitGroup/syntaxsource/blob/71ca82651707ad88fb717f3cc5e106ff62ac3013/syntaxwebsite/app/routes/gametransactions.py#L8
    '''
    self.send_json([])
    return True


@server_path('/productDetails')
@server_path('/marketplace/productDetails')
def _(self: web_server_handler) -> bool:
    '''
    Something to do with developer products.
    https://github.com/essentialsasset/RBLX15/blob/d7c5a76e6c1526e86156410a0b4f024a689920a1/shesnotkewlfgdjkhasdfjhsdf/marketplace/productDetails.php#L4
    '''
    dev_product_id = int(self.query['productId'])
    dev_products = self.game_config.remote_data.dev_products
    dev_product = dev_products.get(dev_product_id)
    if dev_product is None:
        self.send_error(404)
        return True

    self.send_json({
        "AssetId": dev_product.id_num,
        "ProductId": dev_product.id_num,
        "Name": dev_product.name,
        "Description": dev_product.name,
        "AssetTypeId": 19,
        "Creator": 1,
        "IconImageAssetId": 0,
        "Created": 0,
        "Updated": 0,
        "PriceInRobux": 0,
        "PriceInTickets": 0,
        "Sales": 0,
        "IsNew": False,
        "IsForSale": True,
        "IsPublicDomain": False,
        "IsLimited": False,
        "IsLimitedUnique": False,
        "Remaining": False,
        "MinimumMembershipLevel": 0,
        "ContentRatingTypeId": 0,
    })
    return True
