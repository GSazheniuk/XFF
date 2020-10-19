from Model.BaseClasses.BaseAction import BaseAction
import random


def load_from_JSON(data=None, sub_classes=None):
    r = None

    if not sub_classes:
        sub_classes = []

    if "type" in data:
        b = next((sc for sc in sub_classes if sc.__name__ == data["type"]))
        if b:
            r = b()
            r.load_from_JSON(data)

    return r


class BaseObject:
    def __init__(self):
        self.type = type(self).__name__

    def load_from_JSON(self, data=None, sub_classes=None):
        if not sub_classes:
            sub_classes = []

        for p in data:
            if p == "_id":
                self.__setattr__("id", data[p])
            elif type(data[p]) is dict and "type" in data[p]:
                subs = [sc.__name__ for sc in sub_classes]
                if subs and data[p]["type"] in subs:
                    x = next((sc for sc in sub_classes if sc.__name__ == data[p]["type"]))()
                    x.load_from_JSON(data[p], sub_classes)
                    self.__setattr__(p, x)
                else:
                    self.__setattr__(p, data[p])
            else:
                self.__setattr__(p, data[p])

    def dict(self):
        res = {}
        for p in self.__dict__:
            x = eval("self.%s" % p)
            if type(x) is list:
                res[p] = [a.dict() if issubclass(type(a), BaseObject)
                          else a for a in x]
            elif type(x) is dict:
                res[p] = {}
                for a in x:
                    res[p][a] = x[a].dict() if issubclass(type(x[a]), BaseObject) else x[a]
            elif issubclass(type(x), BaseObject):
                res[p] = x.dict()
            elif issubclass(type(x), BaseAction):
                pass
            else:
                res[p if p != 'id' else '_id'] = x
        return res


class BaseMapObject(BaseObject):
    def __init__(self):
        self.point = None
        self.R = 0
        self.objType = None
        self.id = None
        self.status = 0
        self.name = None
        self.scan_rng = 0
        self.atk_rng = 0
        super().__init__()
        pass

    def new(self, point, r, obj_type, object_id, name, scan_rng, atk_rng):
        self.point = point
        self.R = r
        self.objType = obj_type
        self.id = object_id
        self.status = 0
        self.name = name
        self.scan_rng = scan_rng
        self.atk_rng = atk_rng
        pass

    def __del__(self):
        print('MapObject id: %s has been removed...' % self.id)
        pass

    def load_from_JSON(self, data=None, sub_classes=None):
        if not sub_classes:
            sub_classes = []
        sub_classes.append(Point)
        super().load_from_JSON(data, sub_classes)


class Point(BaseObject):
    def __init__(self):
        self.Lat = random.random() * 180 - 90
        self.Long = random.random() * 360 - 180

        super().__init__()
        pass

    def new(self, *args, **kwargs):
        if "lat" in kwargs:
            self.Lat = kwargs["lat"]

        if "long" in kwargs:
            self.Long = kwargs["long"]
