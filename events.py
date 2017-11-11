import config
import random
import BaseMapObject
import map
import MapActions
import SharedData


class Action:
    def __init__(self, action_type, sender, **kwargs):
        self.action_type = action_type
        if action_type == config.MapActionTypes.ACTION_TYPE_APPEAR:
            self._proceed = MapActions.appear
        elif action_type == config.MapActionTypes.ACTION_TYPE_LEAVE:
            self._proceed = MapActions.disappear
        elif action_type == config.MapActionTypes.ACTION_TYPE_MOVE_TO_POINT:
            self._proceed = MapActions.move_to_point

        kwargs['object'] = sender
        self.params = kwargs
        pass

    def proceed(self):
        return self._proceed(**self.params)


class FlyingUFO:
    def __init__(self, o, ms: map.MapSector):
        self.id = random.randint(0, config.EVENTS_MAX_ID)
        self.data = o
        self.map_object = BaseMapObject.BaseMapObject(
            random.randint(0, config.MAP_DEFAULT_SECTOR_WIDTH),
            random.randint(0, config.MAP_DEFAULT_SECTOR_HEIGHT),
            o['diameter'],
            o['ufo_type'],
            self.id
        )
        self.sector = ms
        ms.add_object(self.map_object)
        self.duration = self.get_action_duration_value(config.MapActionTypes.ACTION_TYPE_APPEAR)
        self.action = Action(config.MapActionTypes.ACTION_TYPE_APPEAR, self, **{})
        pass

    def get_action_duration_value(self, action_type):
        if action_type not in self.data['actions']:
            return 0
        else:
            return self.data['actions'][action_type]['max_duration']
        pass

    def next_action(self):
        available_actions = []
        for action in self.data["actions"]:
            available_actions.extend([action] * self.data["actions"][action]["probability"])
            pass
        new_action = available_actions[random.randint(0, len(available_actions) - 1)]

        if new_action == config.MapActionTypes.ACTION_TYPE_MOVE_TO_POINT:
            self.duration = self.data["actions"][new_action]["max_duration"]
            self.action = Action(new_action, self, **{"point": self.sector.get_random_point()})
        elif new_action == config.MapActionTypes.ACTION_TYPE_LEAVE:
            self.duration = self.data["actions"][new_action]["max_duration"]
            self.action = Action(new_action, self, **{})
        pass

    def map_action(self):
        action_result = self.action.proceed()
        if action_result == 1:
            self.next_action()
        elif action_result == -1:
            self.end()
            del SharedData.AllFlyingObjects[self.id]
            pass
        pass

    def tick(self):
        # self.duration -= 1
        if self.action.action_type:
            self.map_action()
        print("event id: %s duration %s" % (self.id, self.duration))
        pass

    def end(self):
        print('end called for %s' % self.id)
        self.sector.remove_object(self.map_object)
        pass

    def __del__(self):
        print(self.id, "-- event ended")
        pass
