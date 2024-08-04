from typing_extensions import Callable, TypeVar, Any
from collections import defaultdict
from queue import Queue

T = TypeVar('T')


class queuer:
    def __init__(self) -> None:
        self.queued_data = defaultdict[Any, Queue[bytes | None]](Queue)
        self.queued_waiters = defaultdict[Any, int](int)

    def get(self, key: T, func: Callable[[T], bytes | None]) -> bytes | None:
        self.queued_waiters[key] += 1
        if self.queued_waiters[key] == 1:
            result = func(key)
            for _ in range(self.queued_waiters[key] - 1):
                self.queued_data[key].put(result)
        else:
            result = self.queued_data[key].get(block=True)

        self.queued_waiters[key] -= 1
        return result
