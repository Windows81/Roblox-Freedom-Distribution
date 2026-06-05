# Standard library imports
import dataclasses
import queue
import uuid

# Typing imports
from typing import Any


@dataclasses.dataclass
class _input_type:
    path: str
    guid: str
    args: tuple[Any, ...]


class obj_type:
    def __init__(self):
        super().__init__()
        self.was_triggered = False
        self.input_queue = queue.Queue[_input_type]()
        self.output_dict = dict[str, queue.Queue[_input_type]]()

    def _generate_guid(self) -> str:
        while True:
            guid = str(uuid.uuid4())
            if guid not in self.output_dict:
                return guid

    def call(self, path: str, game_config, *call_args):
        '''
        This function is accessed by Python scripts which want to interact with RCC servers.
        The function signature should match whatever `gen_function` in `callable.py` specified (as of 2026-06-05).
        '''
        temp_queue = queue.Queue()
        guid = self._generate_guid()
        self.output_dict[guid] = temp_queue

        self.input_queue.put(_input_type(
            path=path,
            guid=guid,
            args=call_args,
        ))

        # Waits for the result to be passed in, then deletes the container to save memory.
        result = temp_queue.get(block=True)
        del self.output_dict[guid]
        return result

    def extract(self) -> dict[str, dict[str, Any]]:
        '''
        This function is accessed by the webserver.
        '''
        self.was_triggered = True
        result = {}
        try:
            item = self.input_queue.get(
                block=True,
                timeout=20,
            )
            val = dataclasses.asdict(item)
            result[item.guid] = val
        except queue.Empty:
            return result

        while True:
            try:
                item = self.input_queue.get_nowait()
            except queue.Empty:
                break
            val = dataclasses.asdict(item)
            result[item.guid] = val

        return result

    def insert(self, data: dict[str, _input_type]) -> None:
        for guid, result in data.items():
            self.output_dict[guid].put(result)
