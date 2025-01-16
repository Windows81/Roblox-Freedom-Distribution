from typing import Any
import dataclasses
import itertools
import queue
import uuid


@dataclasses.dataclass
class _input_type:
    path: str
    guid: str
    args: tuple


class obj_type:
    def __init__(self):
        self.input_queue = queue.Queue[_input_type]()
        self.output_dict = dict[str, queue.Queue]()

    def generate_guid(self) -> str:
        while True:
            guid = str(uuid.uuid4())
            if guid not in self.output_dict:
                return guid

    def call(self, path: str, game_config, *call_args):
        temp_queue = queue.Queue()
        guid = self.generate_guid()
        self.output_dict[guid] = temp_queue

        self.input_queue.put(_input_type(
            path=path,
            guid=guid,
            args=call_args,
        ))

        # Waits for the result to be passed in, then deletes the container to
        # save memory.
        result = temp_queue.get(block=True)
        del self.output_dict[guid]
        return result

    def extract(self) -> dict[str, dict[str, Any]]:
        result = {}
        for i in itertools.count(0):
            try:
                item = self.input_queue.get(
                    block=True,
                    timeout=30 if i == 0 else 1 / 30,
                )
            except queue.Empty:
                break

            val = dataclasses.asdict(item)
            result[item.guid] = val
        return result

    def insert(self, data: dict) -> None:
        for guid, result in data.items():
            self.output_dict[guid].put(result)
