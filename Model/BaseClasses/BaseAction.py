import abc

class BaseAction(abc.ABC):
    def __init__(self, interval):
        self.timeout = 0
        self.interval = interval
        pass

    @abc.abstractmethod
    def start(self):
        pass

    @abc.abstractmethod
    def tick(self):
        pass

    @abc.abstractmethod
    def finish(self):
        pass


class GeoActionStatus:
    INACTIVE = 0
    ACTIVE = 1
    FINISHED = 2