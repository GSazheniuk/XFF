class BaseObject:
    def toJSON(self, obj=None):
        res = '{'
        for p in self.__dict__ if not obj else obj.__dict__:
            if p == "Status":
                print(self.__dict__ if not obj else obj.__dict__)

            x = eval("self.{}".format(p)) if not obj else eval("obj.{}".format(p))
            if not x and x != 0:
                j = "null"
            elif type(x) is list:
                j = "[" + ",".join([self.toJSON(a) if hasattr(a, "__dict__")
                                    else str(a).replace("'", '"') for a in x ]) + "]"
            elif type(x) is dict:
                j = "{" + ",".join(['"{}": {}'.format(a, self.toJSON(x[a])) if hasattr(x[a], "__dict__")
                                    else '"{}": "{}"'.format(a, str(x[a])) for a in x ]) + "}"
            elif type(x) is str:
                j = '"%s"' % x
            else:
                j = self.toJSON(x) if hasattr(x, "__dict__") else str(x)
            res += '"{}": {},'.format(p, j)
        res += '}'
        return res.replace(",}", "}").replace(",]", "]")


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

    def __str__(self):
        return str(self.__dict__)
