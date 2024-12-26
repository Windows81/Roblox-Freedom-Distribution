from web_server._logic import web_server_handler, server_path
import util.versions as versions
import util.const
import util.ssl


@server_path('/game/GetCurrentUser.ashx')
def _(self: web_server_handler) -> bool:
    self.send_data('1')
    return True


@server_path('/login/RequestAuth.ashx')
def _(self: web_server_handler) -> bool:
    self.send_data('%s/login/negotiate.ashx' % self.hostname)
    return True


@server_path('/studio/e.png')
def _(self: web_server_handler) -> bool:
    self.send_data(b'')
    return True


@server_path('/v1.1/Counters/BatchIncrement')
def _(self: web_server_handler) -> bool:
    self.send_data(b'')
    return True
