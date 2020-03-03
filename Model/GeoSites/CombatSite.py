import config
import random
from Geoscape import MapObjects
from Model.Actions.CombatSiteEvents import DeSpawnSiteEvent
import map
import SharedData


class CombatSite:
    def __init__(self, o, ms: map.MapSector):
        self.id = random.randint(0, config.EVENTS_MAX_ID)
        self.data = o
        self.map_object = MapObjects.CombatSiteMO(
            map.Point(),
            self.id,
            o['name']
        )

        self.sector = ms
        ms.add_object(self.map_object)
        self.duration = 20
        self.spawn_event = DeSpawnSiteEvent(self.despawn)
        SharedData.Loop.actions.append(self.spawn_event)
        pass

    def despawn(self):
        self.spawn_event = None
        self.sector.remove_object(self.map_object)
        del SharedData.AllFlyingObjects[self.id]
        pass
