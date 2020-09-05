import config
import random
from Geoscape import MapObjects
import map
from Tools import HelperFunctions
from ActionHandlers import MapActions
from SharedData import SharedData


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
        if o['obj_type'] == config.MapObjectTypes.AIRCRAFT:
            self.map_object = MapObjects.AircraftMO(
                map.Point(),
                o['diameter'],
                self.id,
                o['name']
            )

        if o['obj_type'] == config.MapObjectTypes.COMBAT_SITE:
            self.map_object = MapObjects.CombatSiteMO(
                map.Point(),
                self.id,
                o['name']
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
            new_point = map.Point()
            self.action = Action(new_action, self, **{"point": new_point})
            if config.DEBUG_LEVEL == config.DebugLevels.DEBUG_LEVEL_DETAILED:
                print("Object #%s moving towards (%s, %s) - %s" % (
                    self.id,
                    new_point.Lat,
                    new_point.Long,
                    HelperFunctions.get_location_name(new_point)
                ))
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
            SharedData().remove_ufo(self.id)
            pass
        pass

    def tick(self):
        # self.duration -= 1
        if self.action.action_type:
            self.map_action()
        if config.DEBUG_LEVEL == config.DebugLevels.DEBUG_LEVEL_DETAILED:
            print("event id: %s duration %s" % (self.id, self.duration))
        pass

    def end(self):
        if config.DEBUG_LEVEL == config.DebugLevels.DEBUG_LEVEL_DETAILED:
            print('end called for %s' % self.id)
        self.sector.remove_object(self.map_object)
        pass

    def __del__(self):
        if config.DEBUG_LEVEL == config.DebugLevels.DEBUG_LEVEL_DETAILED:
            print(self.id, "-- event ended")
        pass
