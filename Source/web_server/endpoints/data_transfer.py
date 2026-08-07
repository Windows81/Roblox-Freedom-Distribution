from web_server._logic import web_server_handler, server_path
import json


@server_path("/rfd/data-transfer")
def _(self: web_server_handler) -> bool:
    assert self.is_privileged

    transferer = self.server.data_transferer
    assert transferer is not None

    input_data = json.loads(self.read_content())
    if isinstance(input_data, dict):
        transferer.insert(input_data)

    output_data = transferer.extract()
    self.send_json(output_data)
    return True
