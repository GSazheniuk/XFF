from datetime import datetime
from Model.BaseClasses.BaseAction import ActionStatus
import tornado.gen as gen


class GeoLoop:
    def __init__(self):
        self.actions = []
        self.last_updated = datetime.now()
        pass

    def loop(self):
        while True:
            shooters = [a for a in self.actions if a.timeout == 0]
            next_timeout = 0
            if not shooters:
                timeouters = sorted([a for a in self.actions if a.timeout > 0]
                                    , key=lambda k: k.timeout, reverse=False)
                if timeouters:
                    next_timeout = timeouters[0].timeout
                    for a in timeouters:
                        a.timeout -= next_timeout
                else:
                    next_timeout = 5
            else:
                for a in shooters:
                    if a.status == ActionStatus.INACTIVE:
                        print(a, "Event STARTED!")
                        a.start()

                    if a.status == ActionStatus.ACTIVE and a.timeout == 0:
                        a.tick()

                    if a.status == ActionStatus.FINISHED:
                        a.finish()
                        self.actions.remove(a)
                        print(a, "Event FINISHED!")
                        a = None

            yield next_timeout
        pass  # def

    @gen.coroutine
    def start_loop(self):
        print("Starting loop.")
        for period in self.loop():
            yield gen.sleep(period)
        print("Loop finished.")
        pass
