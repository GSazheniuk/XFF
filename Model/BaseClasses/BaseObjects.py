class BaseObject:
    def load_from_JSON(self, data=None):
        for p in data:
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
            else:
                res[p] = x
        return res


class BaseMapObject(BaseObject):
    def __init__(self, point, r, obj_type, object_id, name):
        self.point = point
        self.R = r
        self.objType = obj_type
        self.id = object_id
        self.status = 0
        self.name = name
        pass

    def __del__(self):
        print('MapObject id: %s has been removed...' % self.id)
        pass
