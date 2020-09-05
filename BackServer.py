import random
import requests

import config
import events
import Waiters

from RTimer import RepeatedTimer
from SharedData import SharedData


def pull_api():
    while True:
        yield requests.get("https://redisq.zkillboard.com/listen.php")


class BackBoneServer:
    rt = {}

    def __init__(self):
        self.active_events = []
        pass

    def start(self):
        self.rt = RepeatedTimer(config.BACKSERVER_TICK_INTERVAL, self._tick)
        # SharedData.Log.save_msg('BackService started... OK')
        pass

    def stop(self):
        self.rt.stop()
        pass

    def _tick(self):
        # available_ufos = self.get_available_ufos(random.randint(0, config.EVENTS_MAX_PROBABILITY))
        # available_sites = self.get_available_sites(random.randint(0, config.EVENTS_MAX_PROBABILITY))

        # for kill in pull_api():
        #     Waiters.all_waiters.deliver_to_waiter(Waiters.WAIT_FOR_TEST, kill)

        if len(SharedData.AllFlyingObjects) >= 15:
            available_ufos = []

        for u in []: # available_ufos:
            ufo = events.FlyingUFO(u, SharedData.Map.DefaultSector)
            SharedData.AllFlyingObjects[ufo.id] = ufo
            pass

        for p in SharedData.Players:
            player = SharedData.Players[p]
            player.tick()
            pass
        pass

    def get_available_ufos(self, probability):
        if config.DEBUG_LEVEL == config.DebugLevels.DEBUG_LEVEL_DETAILED:
            print('probability: %s' % probability)
        return [e for e in SharedData.all_ufos if e['probability'] > probability]

    def get_available_sites(self, probability):
        if config.DEBUG_LEVEL == config.DebugLevels.DEBUG_LEVEL_DETAILED:
            print('probability: %s' % probability)
        return [e for e in SharedData.all_sites if e['probability'] > probability]
