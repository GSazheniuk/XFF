from Tools import HelperFunctions
from Model.BaseClasses.BaseAction import BaseAction, ActionStatus

import config


class AppearAction(BaseAction):
    def __init__(self, **kwargs):
        super().__init__(1, -1)
        self.obj = kwargs["object"] if "object" in kwargs else None
        if self.obj is None:
            if config.DEBUG_LEVEL >= config.DebugLevels.DEBUG_LEVEL_ERRORS_ONLY:
                print('appear error: object is None!')
            self.status = ActionStatus.FINISHED
            return
        self.status = ActionStatus.INACTIVE
        self.obj.map_object.status = kwargs["action_status"] if "action_status" in kwargs else None
        pass

    def start(self):
        if self.status == ActionStatus.INACTIVE:
            self.status = ActionStatus.ACTIVE
        pass

    def tick(self):
        if self.status != ActionStatus.ACTIVE:
            return

        self.obj.duration -= 1

        if self.obj.duration <= 0:
            self.status = ActionStatus.FINISHED

        pass

    def finish(self):
        self.obj.Status = config.UfoStatuses.UFO_STATUS_MOVING
        pass


class MoveAction(BaseAction):
    def __init__(self, **kwargs):
        super().__init__(1, -1)
        self.obj = kwargs["object"] if "object" in kwargs else None
        self.point = kwargs["point"] if "point" in kwargs else None

        if self.point is None or self.obj is None:
            if config.DEBUG_LEVEL >= config.DebugLevels.DEBUG_LEVEL_ERRORS_ONLY:
                print("move_to_point error: point or object is None!")
            self.status = ActionStatus.FINISHED
            return

        self.o, self.mo = self.obj.data, self.obj.map_object
        self.status = ActionStatus.INACTIVE

        if "speed" not in self.o:
            self.o["speed"] = 0
        pass

    def start(self):
        if self.status == ActionStatus.INACTIVE:
            self.status = ActionStatus.ACTIVE
        self.obj.map_object.status = config.UfoStatuses.UFO_STATUS_LEAVING
        pass

    def tick(self):
        if self.status != ActionStatus.ACTIVE:
            return

        if self.o["speed"] < self.o["max_speed"]:
            self.o["speed"] = HelperFunctions.minimum(self.o["speed"] + self.o["acceleration"], self.o["max_speed"])

        dist = HelperFunctions.distance2(self.mo.point, self.point)
        if config.DEBUG_LEVEL == config.DebugLevels.DEBUG_LEVEL_DETAILED:
            print('Distance to point: ', dist)
        self.mo.point = HelperFunctions.next_point(self.mo.point, self.point, self.o["speed"])

        if dist <= self.o["speed"]:
            self.obj.duration = 0
            self.status = ActionStatus.FINISHED
            return

        self.obj.map_object.status = config.UfoStatuses.UFO_STATUS_MOVING
        if config.DEBUG_LEVEL == config.DebugLevels.DEBUG_LEVEL_DETAILED:
            print(self.obj.id, ' moving for next ', self.obj.duration, ' ticks')

        pass

    def finish(self):
        pass
