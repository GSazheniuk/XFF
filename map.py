import random
import config

import Waiters

from Model.BaseClasses.BaseObjects import BaseObject


class MapSector(BaseObject):
    def __init__(self, name, secstat, x, y):
        self._id = random.randint(1000000, 10000000)
        self.Name = name
        self.SecStatus = secstat
        self.X = x
        self.Y = y
        self.Width = config.MAP_DEFAULT_SECTOR_WIDTH
        self.Height = config.MAP_DEFAULT_SECTOR_HEIGHT
        self.objects = {}
        pass

    def add_object(self, o):
        self.objects[o.id] = o
        Waiters.all_waiters.deliver_to_waiter(Waiters.WAIT_FOR_MAP_OBJECTS, o)
        pass

    def remove_object(self, o):
        self.objects[o.id] = None
        del self.objects[o.id]
        Waiters.all_waiters.deliver_to_waiter(Waiters.WAIT_FOR_MAP_OBJECTS, {})
        pass

    def get_objects_on_map(self):
        return self.objects

    def get_objects_on_map_json(self):
        res = '['
        for k in self.objects:
            res += self.objects[k].toJSON() + ','
        res += ']'
        return res.replace(",]", "]")

    def get_id(self):
        return self._id


class Point(BaseObject):
    def __init__(self, lat=None, long=None):
        self.Lat = random.random() * 180 - 90
        self.Long = random.random() * 360 - 180

        if lat:
            self.Lat = lat

        if long:
            self.Long = long
        pass


class Map:
    def __init__(self, w, h):
        self.Width = w
        self.Height = h
        self.AllSectors = []
        self.Sectors = [[MapSector(
            config.MAP_DEFAULT_SECTOR_NAME,
            config.MAP_DEFAULT_SECTOR_SECURITY_STATUS,
            x,
            y) for x in range(w)] for y in range(h)]
        self.DefaultSector = self.Sectors[0][0]
        self.Sector2Waiters = {}
        pass
