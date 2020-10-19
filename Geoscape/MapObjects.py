from Model.BaseClasses.BaseObjects import BaseMapObject
from config import MapObjectTypes


class GroundBaseMO(BaseMapObject):
    def new(self, point, r, object_id, name, obj_type=None, scan_rng=None, atk_rng=None):
        super().new(point, 1, MapObjectTypes.BASE, object_id, name, scan_rng, atk_rng)
        pass


class AircraftMO(BaseMapObject):
    def new(self, point, r, object_id, name, obj_type=None, scan_rng=None, atk_rng=None):
        super(AircraftMO, self).new(point, r, MapObjectTypes.AIRCRAFT, object_id, name, 10, 7)
        pass


class CombatSiteMO(BaseMapObject):
    def __init__(self, point, object_id, name):
        super(CombatSiteMO, self).__init__(point, 1, MapObjectTypes.COMBAT_SITE, object_id, name, 0, 0)
        pass
