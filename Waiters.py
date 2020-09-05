from tornado.concurrent import Future
from Model.BaseClasses.Singleton import Singleton


class AWaiters(metaclass=Singleton):
    WAIT_FOR_CHAT_PLAYERS = 0
    WAIT_FOR_CHAT_MESSAGES = 1
    WAIT_FOR_MAP_OBJECTS = 2
    WAIT_FOR_EVENT_LOG = 3
    WAIT_FOR_TEST = 4
    WAIT_FOR_TIMER = 5
    WAIT_FOR_BUNKER_EVENTS = 6
    WAIT_FOR_BATTLE_EVENTS = 7

    def __init__(self):
        self.waiters = {
            AWaiters.WAIT_FOR_CHAT_PLAYERS: set(),
            AWaiters.WAIT_FOR_CHAT_MESSAGES: set(),
            AWaiters.WAIT_FOR_MAP_OBJECTS: set(),
            AWaiters.WAIT_FOR_EVENT_LOG: set(),
            AWaiters.WAIT_FOR_TEST: set(),
            AWaiters.WAIT_FOR_TIMER: set(),
            AWaiters.WAIT_FOR_BUNKER_EVENTS: set(),
            AWaiters.WAIT_FOR_BATTLE_EVENTS: set(),
        }

    def subscribe(self, waiter_type):
        f = Future()
        self.waiters[waiter_type].add(f)
        return f

    def deliver(self, waiter_type, o):
        w = self.waiters[waiter_type].copy()
        self.waiters[waiter_type].clear()
        for f in w:
            f.set_result(str(o))

    def cancel(self, waiter_type, future):
        self.waiters[waiter_type].remove(future)
        future.set_result({})
