from web_server._logic import web_server_handler, server_path
import json


@server_path("/rfd/data-transfer")
def _(self: web_server_handler) -> bool:
    transferer = self.server.data_transferer
    if not transferer:
        return False

    input_data = json.loads(self.read_content())
    if isinstance(input_data, dict):
        transferer.insert(input_data)

    self.send_json(transferer.extract())
    return True
