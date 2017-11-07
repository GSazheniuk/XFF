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

        for k in SharedData.AllFlyingObjects:
            u = SharedData.AllFlyingObjects[k]
            u.tick()
            if u.duration == 0:
                # u.end()
                # self.active_ufos.remove(u)
                pass
            pass

        for u in available_ufos:
            ufo = events.FlyingUFO(u, SharedData.Map.DefaultSector)
            SharedData.AllFlyingObjects[ufo.id] = ufo
            SharedData.add_map_action(None, ufo, config.MapActionTypes.ACTION_TYPE_APPEAR)
            pass

#        all_actions = SharedData.AllMapActions.values()
        for action_id in list(SharedData.AllMapActions):
            ma = SharedData.AllMapActions[action_id]

            action_result = ma["action"](**ma["kwargs"])
            ufo = ma["kwargs"]["object"]

            if action_result == 1:
                available_actions = []
                for action in ufo.data["actions"]:
                    available_actions.extend([action]*ufo.data["actions"][action]["probability"])
                print(available_actions)
                new_action = available_actions[random.randint(0, len(available_actions)-1)]
                print("New Action: ", new_action)

                SharedData.add_map_action(None, ufo, new_action)
                pass

            if action_result == -1:
                ufo.end()
                del SharedData.AllFlyingObjects[ufo.id]
                pass

            if action_result != 0:
                SharedData.AllMapActions[action_id] = None
                del SharedData.AllMapActions[action_id]
                pass
            pass

        Waiters.all_waiters.deliver_to_waiter(Waiters.WAIT_FOR_MAP_OBJECTS, {})
        pass

    def get_available_ufos(self, probability):
        print('probability: %s' % probability)
        return [e for e in self.all_ufos if e['probability'] > probability]
