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


@server_path(r'/v1/users/(\d+)/items/gamepass/(\d+)', regex=True, commands={'GET'})
def _(self: web_server_handler, match: re.Match[str]) -> bool:
    '''
    https://github.com/SushiDesigner/Meteor-back/blob/dc561b5af196ca9c375530d30d593fc8d7f0486c/routes/marketplace.js#L129
    '''
    user_id_num = int(match.group(1))
    gamepass_id = int(match.group(2))
    gamepass_catalogue = self.game_config.remote_data.gamepasses

    has_gamepass = self.server.storage.gamepasses.check(
        user_id_num,
        gamepass_id,
    )

    data = (
        [
            {
                "type": "GamePass",
                "id": gamepass_id,
                "name": gamepass_catalogue.get(gamepass_id),
                "instanceId": None,
            }
        ]
        if has_gamepass else
        []
    )

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
