import random
import config

import Waiters


class MapSector:
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
        self.objects[o.id] = o.get_dict()
        Waiters.all_waiters.deliver_to_waiter(Waiters.WAIT_FOR_MAP_OBJECTS, o)
        pass

    def remove_object(self, o):
        self.objects[o.id] = None
        del self.objects[o.id]
        Waiters.all_waiters.deliver_to_waiter(Waiters.WAIT_FOR_MAP_OBJECTS, {})
        pass

    def get_objects_on_map(self):
        return self.objects

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
