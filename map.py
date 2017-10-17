import random
import config

from tornado.concurrent import Future


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
        self.Waiters = set()
        pass

    def add_object(self, o):
        self.objects[o.id] = o.get_dict()
        if len(self.Waiters) > 0:
            for future in self.Waiters:
                future.set_result(self.objects)
        self.Waiters = set()
        pass

    def remove_object(self, o):
        self.objects[o.id] = None
        if len(self.Waiters) > 0:
            for future in self.Waiters:
                future.set_result(self.objects)
        self.Waiters = set()
        pass

    def get_objects_on_map(self):
        result_future = Future()
        self.Waiters.add(result_future)
        return result_future

    def cancel_wait(self, future):
        self.Waiters.remove(future)
        future.set_result({})
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
