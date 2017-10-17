import config
import random


class BaseMapObject:
    def __init__(self, x, y, r, obj_type):
        self.X = x
        self.Y = y
        self.R = r
        self.objType = obj_type
        self.id = random.randint(0, config.EVENTS_MAX_ID)
        pass

    def __del__(self):
        print('MapObject id: %s has been removed...' % self.id)
        pass

    def __str__(self):
        return self.__dict__

    def get_dict(self):
        return self.__dict__
