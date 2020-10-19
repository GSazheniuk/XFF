import uuid
import random

from Assets.crew import Soldier
from Model.BaseClasses.BaseObjects import *
from Model.Havens.Buildings.AllBuildings import all_buildings
from Geoscape.MapObjects import GroundBaseMO
from SharedData import SharedData


class BaseHaven(BaseObject):
    def __init__(self):
        self.id = uuid.uuid4().hex
        self.name = ""
        self.allowed_buildings = []
        self.building_spots = []
        self.buildings = {}
        self.map_object = None
        self.avail_recruits = []
        self.refresh_event = None
        super().__init__()

    def new(self, *args, **kwargs):
        point, scan_rng, atk_rng = None, 0, 0
        for k in kwargs:
            if k == "point":
                point = kwargs[k]
            elif k == "scan_rng":
                scan_rng = kwargs[k]
            elif k == "atk_rng":
                atk_rng = kwargs[k]
            else:
                self.__setattr__(k, kwargs[k])

        if point:
            self.map_object = GroundBaseMO(point, self.id, self.name, scan_rng, atk_rng)

    def save(self):
        SharedData().save_haven(haven=self)

    def refresh_recruits(self):
        self.avail_recruits = []
        for i in range(5):
            s = Soldier("Rookie {}".format(random.randint(0, 100)))
            self.avail_recruits.append(s)
        pass

    def clear_recruits(self):
        self.avail_recruits = []
        pass

    def load_from_JSON(self, data=None, sub_classes=None):
        if not sub_classes:
            sub_classes = []
        sub_classes.append(GroundBaseMO)
        sub_classes.extend(all_buildings)
        super().load_from_JSON(data, sub_classes)
