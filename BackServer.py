import random

import SharedData
import UFOs
import config
import events
import Waiters

from RTimer import RepeatedTimer
from Tools import mongohelper


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

        # Load Collections from Mongo
        self.all_ufos = self.m_helper.get_all_ufos()
        print(self.all_ufos)
        pass

    def start(self):
        self.rt = RepeatedTimer(config.BACKSERVER_TICK_INTERVAL, self._tick)
        SharedData.Log.save_msg('BackService started... OK')
        pass

    def stop(self):
        self.rt.stop()
        pass

    def _tick(self):
        available_ufos = self.get_available_ufos(random.randint(0, config.EVENTS_MAX_PROBABILITY))

        for k in list(SharedData.AllFlyingObjects):
            u = SharedData.AllFlyingObjects[k]
            u.tick()
            pass

        for u in available_ufos:
            ufo = events.FlyingUFO(u, SharedData.Map.DefaultSector)
            SharedData.AllFlyingObjects[ufo.id] = ufo
            pass

        Waiters.all_waiters.deliver_to_waiter(Waiters.WAIT_FOR_MAP_OBJECTS, {})
        pass

    def get_available_ufos(self, probability):
        print('probability: %s' % probability)
        return [e for e in self.all_ufos if e['probability'] > probability]
