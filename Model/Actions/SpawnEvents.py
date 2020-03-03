from Model.BaseClasses.BaseAction import BaseAction, ActionStatus
from Model.GeoSites.CombatSite import CombatSite
import Waiters
import SharedData
import random
import config


class SpawnSiteEvent(BaseAction):
    def __init__(self):
        super().__init__(20, -1)
        self.status = ActionStatus.INACTIVE
        pass

    def start(self):
        if self.status == ActionStatus.INACTIVE:
            self.status = ActionStatus.ACTIVE
            self.timeout = self.interval
        pass

    def tick(self):
        if self.status != ActionStatus.ACTIVE:
            return

        probability = random.randint(0, config.EVENTS_MAX_PROBABILITY)
        sites = [e for e in SharedData.all_sites if e['probability'] > probability]
        for u in sites:
            site = CombatSite(u, SharedData.Map.DefaultSector)
            SharedData.AllFlyingObjects[site.id] = site
            pass

        Waiters.all_waiters.deliver_to_waiter(Waiters.WAIT_FOR_MAP_OBJECTS, {})

        self.timeout = self.interval
        pass

    def finish(self):
        pass
