from Model.BaseClasses.BaseAction import BaseAction, ActionStatus
from Waiters import AWaiters


class RefreshRecruitsEvent(BaseAction):
    def __init__(self, callback):
        super().__init__(30, 1)
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

        if self.ticks > 0:
            self.ticks -= 1

        if self.ticks == 0:
            self.status = ActionStatus.FINISHED
            return

        self.timeout = self.interval
        AWaiters().deliver(AWaiters.WAIT_FOR_BUNKER_EVENTS, True)
        pass

    def finish(self):
        self.callback()
        pass
