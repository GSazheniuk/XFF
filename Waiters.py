from tornado.concurrent import Future

WAIT_FOR_CHAT_PLAYERS = 0
WAIT_FOR_CHAT_MESSAGES = 1
WAIT_FOR_MAP_OBJECTS = 2
WAIT_FOR_EVENT_LOG = 3
WAIT_FOR_TEST = 4
WAIT_FOR_TIMER = 5


class Waiters:
    def __init__(self):
        self._all_waiters = {
            WAIT_FOR_CHAT_PLAYERS: set(),
            WAIT_FOR_CHAT_MESSAGES: set(),
            WAIT_FOR_MAP_OBJECTS: set(),
            WAIT_FOR_EVENT_LOG: set(),
            WAIT_FOR_TEST: set(),
            WAIT_FOR_TIMER: set(),
        }
        pass

    def subscribe_waiter(self, waiter_type):
        result_future = Future()
        self._all_waiters[waiter_type].add(result_future)
        return result_future

    def deliver_to_waiter(self, waiter_type, o):
        for future in self._all_waiters[waiter_type]:
            future.set_result(o)
            pass
        self._all_waiters[waiter_type] = set()
        pass

    def cancel_waiter(self, waiter_type, future):
        self._all_waiters[waiter_type].remove(future)
        future.set_result({})
        pass


all_waiters = Waiters()
