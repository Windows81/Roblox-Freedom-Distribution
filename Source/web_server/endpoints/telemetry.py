from web_server._logic import web_server_handler, server_path


@server_path(r'/client/pbe')
@server_path(r'/mobile/pbe')
@server_path(r'/studio/pbe')
def _(self: web_server_handler) -> bool:
    self.send_response(200)
    self.send_header('Content-type', 'application/json')
    self.send_json({})
    return True

@server_path(r'/v1/enrollments')
def _(self: web_server_handler) -> bool:
    self.send_response(200)
    self.send_header('Content-type', 'application/json')
    self.send_json({
        "SubjectType": "BrowserTracker",
        "SubjectTargetId": 63713166375,
        "ExperimentName": "AllUsers.DevelopSplashScreen.GreenStartCreatingButton",
        "Status": "Inactive",
        "Variation": None
    })
    return True

@server_path(r'/v1/get-enrollments')
def _(self: web_server_handler) -> bool:
    self.send_response(200)
    self.send_header('Content-type', 'application/json')
    self.send_json({})
    return True