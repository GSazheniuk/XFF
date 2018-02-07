import config
import map
import random

from BaseMapObject import BaseMapObject


class Bunker:
    def __init__(self, name, organization, sector: map.MapSector):
        self.ObjectName = name
        self.Organization = organization
        self.CurrentSector = sector

        self.MapObject = BaseMapObject(
            x=random.randint(0, config.MAP_DEFAULT_SECTOR_WIDTH),
            y=random.randint(0, config.MAP_DEFAULT_SECTOR_HEIGHT),
            r=5,
            obj_type=config.MapObjectTypes.NPC_ORG_HQS,
            object_id=random.randint(0, config.EVENTS_MAX_ID),
            name=name
        )
        sector.add_object(self.MapObject)
        pass

    def get_id(self):
        return self.MapObject.id
