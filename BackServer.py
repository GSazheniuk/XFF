import random
import time
import config

import mongohelper
import events
import UFOs
import SharedData

from RTimer import RepeatedTimer


class BackBoneServer:
    rt = {}

    def __init__(self):
        self.active_events = []
        self.active_ufos = []
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

        for u in self.active_ufos[:]:
            u.tick()
            if u.duration == 0:
                u.end()
                self.active_ufos.remove(u)
            pass

        for u in available_ufos:
            self.active_ufos.append(events.FlyingUFO(u, SharedData.Map.DefaultSector))
            pass
        pass

    def get_available_ufos(self, probability):
        print('probability: %s' % probability)
        return [e for e in self.all_ufos if e['probability'] > probability]
