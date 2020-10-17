from Model.BaseClasses.BaseAction import BaseAction


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
    def __init__(self, point, r, obj_type, object_id, name, scan_rng, atk_rng):
        self.point = point
        self.R = r
        self.objType = obj_type
        self.id = object_id
        self.status = 0
        self.name = name
        self.scan_rng = scan_rng
        self.atk_rng = atk_rng
        super().__init__()
        pass

    def __del__(self):
        print('MapObject id: %s has been removed...' % self.id)
        pass
