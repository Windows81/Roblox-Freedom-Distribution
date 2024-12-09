from typing_extensions import Callable, TypeVar, Any
from collections import defaultdict
from queue import Queue

T = TypeVar('T')


class queuer:
    def __init__(self) -> None:
        # Dictionary to store queues for each key.
        self.queued_data = defaultdict[Any, Queue[bytes | None]](Queue)
        # Dictionary to keep track of the number of waiters for each key.
        self.queued_waiters = defaultdict[Any, int](int)

    def get(self, key: T, func: Callable[[T], bytes | None]) -> bytes | None:
        # Increments the number of waiters for this key.
        self.queued_waiters[key] += 1
        if self.queued_waiters[key] == 1:
            result = func(key)
            # If this is the first waiter, puts the result in the queue for this key.
            for _ in range(self.queued_waiters[key] - 1):
                self.queued_data[key].put(result)
        else:
            # If there are already waiters, gets the result from the queue for this key.
            result = self.queued_data[key].get(block=True)

        self.queued_waiters[key] -= 1
        return result
