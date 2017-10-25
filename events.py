import config
import random
import BaseMapObject

import FlyingObjects


class BaseEvent:
    def __init__(self, probability, duration):
        self.probability = probability
        self.duration = duration
        self.id = random.randint(0, config.EVENTS_MAX_ID)
        self.objects = []
        self.sector = None
        pass

    def tick(self):
        self.duration -= 1
        print("event id: %s duration %s" % (self.id, self.duration))
        pass

    def end(self):
        print('end called for %s' % self.id)
        for o in self.objects:
            self.sector.remove_object(o)
        pass

    def __del__(self):
        print(self.id, "-- event ended")
        pass


class SmallUFO(BaseEvent):
    def __init__(self, ms):
        super(SmallUFO, self).__init__(config.EVENTS_SMALL_UFO_PROBABILITY, config.EVENTS_SMALL_UFO_DURATION)
        o = FlyingObjects.FlyingSmallUFO(random.randint(0, ms.X), random.randint(0, ms.Y))
        self.objects.append(o)
        self.sector = ms
        ms.add_object(o)
        print('Event Created')
        print(self.id)
        print(o.id)
        pass


class FlyingUFO:
    def __init__(self, o, ms):
        self.duration = o['duration']
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
        print('%s appeared in %s (%s) for %s ticks' % (o['ufo_type'], ms.Name, self.id, self.duration))
        print(self.id)
        print(o['_id'])
        pass

    def tick(self):
        self.duration -= 1
        print("event id: %s duration %s" % (self.id, self.duration))
        pass

    def end(self):
        print('end called for %s' % self.id)
        self.sector.remove_object(self.map_object)
        pass

    def __del__(self):
        print(self.id, "-- event ended")
        pass
