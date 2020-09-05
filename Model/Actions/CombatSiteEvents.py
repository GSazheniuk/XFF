from Model.BaseClasses.BaseAction import BaseAction, ActionStatus
from Waiters import AWaiters


class DeSpawnSiteEvent(BaseAction):
    def __init__(self, callback):
        super().__init__(20, 5)
        self.callback = callback
        self.status = ActionStatus.INACTIVE
        pass

    def start(self):
        if self.status == ActionStatus.INACTIVE:
            self.status = ActionStatus.ACTIVE
            self.timeout = self.interval
        pass

    def tick(self):
        if self.status != ActionStatus.ACTIVE:
            return

        if self.ticks:
            self.ticks -= 1
        else:
            self.status = ActionStatus.FINISHED

        AWaiters().deliver(AWaiters.WAIT_FOR_MAP_OBJECTS, {})

        self.timeout = self.interval
        pass

    def finish(self):
        self.callback()
        pass
