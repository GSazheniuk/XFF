from Model.BaseClasses.BaseAction import BaseAction, ActionStatus
import datetime as dt
from Waiters import AWaiters


class TimeAction(BaseAction):
    def __init__(self):
        super().__init__(1, -1)
        self.current_time = dt.datetime(2047, 1, 1, 0, 0, 0)
        self.status = ActionStatus.INACTIVE
        pass

    def start(self):
        if self.status == ActionStatus.INACTIVE:
            self.status = ActionStatus.ACTIVE
        pass

    def tick(self):
        if self.status != ActionStatus.ACTIVE:
            return

        self.current_time += dt.timedelta(seconds=5)
        self.timeout = self.interval
        AWaiters().deliver(AWaiters.WAIT_FOR_TIMER, self.current_time.strftime("%Y-%b-%d %H:%M:%S"))
        pass

    def finish(self):
        self.status = ActionStatus.FINISHED
        pass
