import config
import random

from BaseMapObject import BaseMapObject


class FlyingSmallUFO(BaseMapObject):
    def __init__(self, x, y):
        super(FlyingSmallUFO, self).__init__(
            x,
            y,
            config.MAP_OBJECTS_FLYING_SMALL_UFO_RADIUS,
            config.MapObjectTypes.SMALL_FLYING_UFO
        )
        pass
