import random
import requests

import SharedData
from Model.MongoCollections import UFOs, GroundSite
import config
import events
import Waiters

from RTimer import RepeatedTimer
from Tools import mongohelper


def pull_api():
    while True:
        yield requests.get("https://redisq.zkillboard.com/listen.php")


class BackBoneServer:
    rt = {}

    def __init__(self):
        self.active_events = []
        self.m_helper = mongohelper.MongoHelper()

        # Populate UFOs collection with default objects
        if config.BACKSERVER_POPULATE_MONGO:
            self.m_helper.add_ufo(UFOs.Probe())
            self.m_helper.add_ufo(UFOs.SmallScout())
            self.m_helper.add_ufo(UFOs.MediumScout())
            self.m_helper.add_ufo(UFOs.LargeScout())
            self.m_helper.add_site(GroundSite.BasicSectoidOperation())

        # Load Collections from Mongo
        self.all_ufos = self.m_helper.get_all_ufos()
        self.all_sites = self.m_helper.get__all_sites()
        if config.DEBUG_LEVEL >= config.DebugLevels.DEBUG_LEVEL_INFO:
            print(self.all_ufos)
            print(self.all_sites)
        pass

    def start(self):
        self.rt = RepeatedTimer(config.BACKSERVER_TICK_INTERVAL, self._tick)
        # SharedData.Log.save_msg('BackService started... OK')
        pass

    def stop(self):
        self.rt.stop()
        pass

    def _tick(self):
        available_ufos = self.get_available_ufos(random.randint(0, config.EVENTS_MAX_PROBABILITY))
        available_sites = self.get_available_sites(random.randint(0, config.EVENTS_MAX_PROBABILITY))

        # for kill in pull_api():
        #     Waiters.all_waiters.deliver_to_waiter(Waiters.WAIT_FOR_TEST, kill)

        if len(SharedData.AllFlyingObjects) >= 15:
            available_ufos = []

        for k in list(SharedData.AllFlyingObjects):
            u = SharedData.AllFlyingObjects[k]
            u.tick()
            pass

        for u in available_ufos:
            ufo = events.FlyingUFO(u, SharedData.Map.DefaultSector)
            SharedData.AllFlyingObjects[ufo.id] = ufo
            pass

        for u in available_sites:
            site = events.FlyingUFO(u, SharedData.Map.DefaultSector)
            SharedData.AllFlyingObjects[site.id] = site
            pass

        Waiters.all_waiters.deliver_to_waiter(Waiters.WAIT_FOR_MAP_OBJECTS, {})

        for p in SharedData.Players:
            player = SharedData.Players[p]
            player.tick()
            pass
        pass

    def get_available_ufos(self, probability):
        if config.DEBUG_LEVEL == config.DebugLevels.DEBUG_LEVEL_DETAILED:
            print('probability: %s' % probability)
        return [e for e in self.all_ufos if e['probability'] > probability]

    def get_available_sites(self, probability):
        if config.DEBUG_LEVEL == config.DebugLevels.DEBUG_LEVEL_DETAILED:
            print('probability: %s' % probability)
        return [e for e in self.all_sites if e['probability'] > probability]
