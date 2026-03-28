import util.auth
import util.versions as versions
from web_server._logic import web_server_handler, server_path


@server_path('/v1/users/authenticated')
def _(self: web_server_handler) -> bool:
    return util.auth.HandleAuthenticatedUserEndpoint(self)


@server_path(r'/signup/is-username-valid', versions={versions.rōblox.v463}, commands={'GET'})
def _(self: web_server_handler) -> bool:
    username = (
        self.query.get("username") or
        self.query.get("value") or
        ""
    ).strip()
    message = util.auth.ValidateUsername(self.server.storage, username)
    self.send_json({
        "code": 1 if message is None else 0,
        "message": message or "Username is valid",
    })
    return True


@server_path(r'/signup/is-password-valid', versions={versions.rōblox.v463}, commands={'GET'})
def _(self: web_server_handler) -> bool:
    password = self.query.get("password") or ""
    message = util.auth.ValidatePasswordString(password)
    self.send_json({
        "code": 1 if message is None else 0,
        "message": message or "Password is valid",
    })
    return True


@server_path('/v1/login')
def _(self: web_server_handler) -> bool:
    return util.auth.HandleLogin(self)


@server_path('/v2/signup')
def _(self: web_server_handler) -> bool:
    return util.auth.HandleSignup(self)


@server_path('/v2/twostepverification/verify', commands={'POST'})
def _(self: web_server_handler) -> bool:
    return util.auth.HandleTwoStepVerification(self)


@server_path('/Login/NewAuthTicket', commands={'POST'})
@util.auth.authenticated_required_api
def _(self: web_server_handler) -> bool:
    return util.auth.HandleLoginNewAuthTicket(self)


@server_path('/game/logout.aspx', commands={'GET'})
@util.auth.authenticated_required
def _(self: web_server_handler) -> bool:
    return util.auth.HandleLogoutRedirect(self)


@server_path('/v1/logout', commands={'POST'})
@server_path('/v2/logout', commands={'POST'})
@util.auth.authenticated_required_api
def _(self: web_server_handler) -> bool:
    return util.auth.HandleLogoutApi(self)


@server_path('/v2/passwords/current-status', commands={'GET'})
@util.auth.authenticated_required_api
def _(self: web_server_handler) -> bool:
    return util.auth.HandlePasswordsCurrentStatus(self)
