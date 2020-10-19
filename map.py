import random
import config

from Waiters import AWaiters

from Model.BaseClasses.BaseObjects import BaseObject, BaseMapObject


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
        super().__init__()
        pass

    def add_object(self, o):
        if not o:
            return
        if type(o) is dict:
            mo = BaseMapObject()
            mo.load_from_JSON(o)
            o = mo
        self.objects[o.id] = o
        AWaiters().deliver(AWaiters.WAIT_FOR_MAP_OBJECTS, o)
        pass

    def remove_object(self, o):
        self.objects[o.id] = None
        del self.objects[o.id]
        AWaiters().deliver(AWaiters.WAIT_FOR_MAP_OBJECTS, {})
        pass

    def get_objects_on_map(self):
        return self.objects

    def get_objects_on_map_json(self):
        res = {
            "objects": [self.objects[x].dict() for x in self.objects]
        }
        # res = '['
        # for k in self.objects:
        #     res += str(self.objects[k].dict()) + ','
        # res += ']'
        # return res.replace(",]", "]")
        return res

    def get_id(self):
        return self._id


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
