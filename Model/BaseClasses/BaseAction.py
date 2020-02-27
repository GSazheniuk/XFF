import abc

class BaseAction(abc.ABC):
    def __init__(self, interval, ticks):
        self.timeout = 0
        self.ticks = ticks
        self.interval = interval
        pass

    def toJSON(self):
        return self.timeout

    @abc.abstractmethod
    def start(self):
        pass

    @abc.abstractmethod
    def tick(self):
        pass

    @abc.abstractmethod
    def finish(self):
        pass


class ActionStatus:
    INACTIVE = 0
    ACTIVE = 1
    FINISHED = 2