from collections import defaultdict
from typing import Callable, Any
from queue import Queue


class queuer[T]:
    '''
    When muliple threads try to call the same function at the same time,
    This wrapper dictionary class organises it such that only one of the functions is called at a time.
    '''

    def __init__(self) -> None:
        super().__init__()
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
