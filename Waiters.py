from tornado.concurrent import Future

WAIT_FOR_CHAT_PLAYERS = 0
WAIT_FOR_CHAT_MESSAGES = 1
WAIT_FOR_MAP_OBJECTS = 2
WAIT_FOR_EVENT_LOG = 3


class Waiters:
    def __init__(self):
        self._all_waiters = {
            WAIT_FOR_CHAT_PLAYERS: set(),
            WAIT_FOR_CHAT_MESSAGES: set(),
            WAIT_FOR_MAP_OBJECTS: set(),
            WAIT_FOR_EVENT_LOG: set(),
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

    def subscribe_for_chat_messages(self):
        result_future = Future()
        self._ChatMessageWaiters.add(result_future)
        return result_future

    def subscribe_for_map_sector_objects(self):
        result_future = Future()
        self._MapSectorObjectWaiters.add(result_future)
        return result_future

    def subscribe_for_event_log(self):
        result_future = Future()
        self._EventLogWaiters.add(result_future)
        return result_future

    def send_to_chat_message_waiters(self, o):
        for future in self._ChatMessageWaiters:
            future.set_result(o)
            pass
        self._ChatMessageWaiters = set()
        pass

    def send_to_map_sector_object_waiters(self, o):
        for future in self._MapSectorObjectWaiters:
            future.set_result(o)
            pass
        self._MapSectorObjectWaiters = set()
        pass

    def send_to_event_log_waiters(self, o):
        for future in self._EventLogWaiters:
            future.set_result(o)
            pass
        self._EventLogWaiters = set()
        pass

    def cancel_chat_message_waiters(self, future):
        self._ChatMessageWaiters.remove(future)
        future.set_result({})
        pass


all_waiters = Waiters()
