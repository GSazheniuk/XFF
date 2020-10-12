import uuid
from Model.BaseClasses.BaseObjects import BaseObject
from SharedData import SharedData


class BaseBuilding(BaseObject):
    def __init__(self):
        self.id = uuid.uuid4().hex
        self.haven_id = None
        self.name = ""
        self.type = None
        self.power_usage = 0
        self.map_object = None
        self.required_space = 0
        self.condition = 0
        self.maintenance_req = 0
        self.coos = []

    def new(self, *args, **kwargs):
        for k in kwargs:
            self.__setattr__(k, kwargs[k])

    def save(self):
        haven = SharedData().havens[self.haven_id]
        haven.save()
