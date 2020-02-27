from Model.BaseClasses.BaseAction import BaseAction, GeoActionStatus
import datetime as dt
import Waiters


class TimeAction(BaseAction):
    def __init__(self):
        super().__init__(1)
        self.current_time = dt.datetime(2047, 1, 1, 0, 0, 0)
        self.status = GeoActionStatus.INACTIVE
        pass

    def start(self):
        if self.status == GeoActionStatus.INACTIVE:
            self.status = GeoActionStatus.ACTIVE
        pass

    def tick(self):
        if self.status != GeoActionStatus.ACTIVE:
            return

        self.current_time += dt.timedelta(seconds=5)
        self.timeout = self.interval
        Waiters.all_waiters.deliver_to_waiter(Waiters.WAIT_FOR_TIMER, self.current_time)
        pass

    def finish(self):
        self.status = GeoActionStatus.FINISHED
        pass
