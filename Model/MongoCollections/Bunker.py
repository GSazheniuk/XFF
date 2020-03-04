import config
import map
import random

from Model.BaseClasses.BaseObjects import BaseObject
from Geoscape.MapObjects import GroundBaseMO
from Assets.crew import Soldier


class Bunker(BaseObject):
    def __init__(self, name, organization, sector: map.MapSector):
        self.ObjectName = name
        # self.Organization = organization
        self.CurrentSector = sector
        self.avail_recruits = []
        self.refresh_event = None

        self.MapObject = GroundBaseMO(
            point=map.Point(),
            object_id=random.randint(0, config.EVENTS_MAX_ID),
            name=name
        )
        sector.add_object(self.MapObject)
        pass

    def get_id(self):
        return self.MapObject.id

    def refresh_recruits(self):
        self.avail_recruits = []
        for i in range(5):
            s = Soldier("Rookie {}".format(random.randint(0, 100)))
            self.avail_recruits.append(s)
        pass

    def clear_recruits(self):
        self.avail_recruits = []
        pass
