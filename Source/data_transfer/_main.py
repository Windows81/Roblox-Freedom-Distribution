
from typing import Any, Callable
import functools
import itertools
import queue
import uuid
import attr

SCRIPT_FORMAT = """
print('Initialised RFD server scripts.')
_G.RFD = {%(functions)s}
spawn(function()
    local BaseUrl = game:GetService("ContentProvider").BaseUrl:lower()
    local HttpRbxApiService = game:GetService("HttpRbxApiService")
    local HttpService = game:GetService("HttpService")
    local Results = {}
    local Url = BaseUrl .. "rfd/data-transfer"
    while true do
    	local Calls = HttpRbxApiService:PostAsync(Url, HttpService:JSONEncode(Results))
    	Results = {}
    	for guid, data in next, HttpService:JSONDecode(Calls) do
    		local path, args = data.path, data.args
            print(path, unpack(args))
    		Results[guid] = _G.RFD[path](unpack(args))
    	end
    end
end)
"""


@attr.dataclass
class _input_type:
    path: str
    guid: str
    args: tuple


class transferer:
    def __init__(self):
        self.input_queue = queue.Queue[_input_type]()
        self.output_dict = dict[str, queue.Queue]()

    def generate_guid(self) -> str:
        while True:
            guid = str(uuid.uuid4())
            if guid not in self.output_dict:
                return guid

    def call(self, path: str, game_config, *a):
        output_queue = queue.Queue()
        guid = self.generate_guid()
        self.output_dict[guid] = output_queue

        self.input_queue.put(_input_type(
            path=path,
            guid=guid,
            args=a,
        ))

        # Waits for the result to be passed in, then deletes the container to save memory.
        result = output_queue.get(block=True)
        del self.output_dict[guid]
        return result

    def extract(self) -> dict[str, dict[str, Any]]:
        result = {}
        for i in itertools.count(0):
            try:
                item = self.input_queue.get(
                    block=True,
                    timeout=30 if i == 0 else 0.2,
                )
            except queue.Empty:
                break

            val = attr.asdict(item)
            result[item.guid] = val
        return result

    def insert(self, data: dict) -> None:
        for guid, result in data.items():
            self.output_dict[guid].put(result)


@functools.cache
def list_functions(game_config) -> dict:
    return {
        key: ann
        for key, ann in game_config.flatten().items()
        if getattr(ann.typ, '_name', None) == 'Callable'
    }


@functools.cache
def get_rcc_routine(game_config) -> str:
    return SCRIPT_FORMAT % {
        'functions': '\n'.join(
            f'["{ann.path}"] = ({ann.rep});'
            for ann in list_functions(game_config).values()
        )
    }
