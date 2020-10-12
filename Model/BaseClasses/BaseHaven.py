import uuid
from Model.BaseClasses.BaseObjects import BaseObject, BaseMapObject
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


def load_havens():
    print("Loading Havens...")
    for o in SharedData().mongo_helper.Havens.find():
        haven = BaseHaven()
        haven.load_from_JSON(o)
        SharedData().havens[haven.id] = haven
        SharedData().add_base(haven)
    print("\bOK")


load_havens()
