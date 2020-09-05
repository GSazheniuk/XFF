from Model.BaseClasses.BaseAction import BaseAction, ActionStatus
from Model.GeoSites.CombatSite import CombatSite
from Waiters import AWaiters
from SharedData import SharedData


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
        SharedData().spawn_combat_sites(CombatSite)
        AWaiters().deliver(AWaiters.WAIT_FOR_MAP_OBJECTS, {})
        self.timeout = self.interval

    def finish(self):
        pass
