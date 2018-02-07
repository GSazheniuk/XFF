class BaseMapObject:
    def __init__(self, x, y, r, obj_type, object_id, name):
        self.X = x
        self.Y = y
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
        return self.__dict__

    def get_dict(self):
        return self.__dict__
