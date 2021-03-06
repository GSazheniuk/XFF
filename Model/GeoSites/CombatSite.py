import config
import random
import map
import tornado.gen as gen
import math

from Geoscape import MapObjects
from Model.Actions.CombatSiteEvents import DeSpawnSiteEvent
from Model.BaseClasses.BaseObjects import Point
from PlayerClass import Player
from Assets.crew import Sectoid
from Waiters import AWaiters
from SharedData import SharedData


class CombatSite:
    def __init__(self, o, ms: map.MapSector):
        self.id = random.randint(0, config.EVENTS_MAX_ID)
        self.data = o
        self.map_object = MapObjects.CombatSiteMO()
        p = Point()
        p.new()
        self.map_object.new(
            p,
            self.id,
            o['name']
        )

        self.sector = ms
        self.Crew = []
        self.log = []
        ms.add_object(self.map_object)
        self.duration = 20
        self.spawn_event = DeSpawnSiteEvent(self.despawn)
        SharedData().add_action(self.spawn_event)
        pass

    def battle_loop(self, pl: Player):
        all_p = pl.Crew + self.Crew
        for a in all_p:
            a.x = random.randint(0, 20)
            a.y = random.randint(0, 20)

        print("Battle for {} started.".format(self.id))
        for i in range(3):
            yield 1

        rnd = 1
        AWaiters().deliver(AWaiters.WAIT_FOR_BATTLE_EVENTS, "Battle for {} started.".format(self.id))
        while len([x for x in pl.Crew if x.health]) > 0 and len([y for y in self.Crew if y.health]) > 0:
            shooters = sorted([p for p in all_p
                               if
                               p.timeout == 0 and p.time_units >= min([a.cost for a in p.right_arm.shots]) and p.health]
                              , key=lambda k: k.reaction, reverse=True)
            next_timeout = 0
            if not shooters:
                timeouters = sorted([p for p in all_p
                                     if p.timeout > 0]
                                    , key=lambda k: k.timeout, reverse=False)
                if timeouters:
                    next_timeout = timeouters[0].timeout
                    for p in timeouters:
                        p.timeout -= next_timeout
                else:
                    next_timeout = 1
            else:
                for p in shooters:
                    if not p.health:
                        continue
                    wep = p.right_arm
                    e = [x for x in all_p if x.team != p.team and x.health]

                    if not e:
                        continue

                    e = sorted(e
                               , key=lambda k: max([s.calc_shot_chance(wep.range
                                                                       , math.sqrt(math.pow(p.x - k.x, 2)
                                                                                   + math.pow(p.y - k.y, 2))
                                                                       , p.accuracy) for s in wep.shots])
                               , reverse=True)[0]
                    dist = math.sqrt(math.pow(p.x - e.x, 2) + math.pow(p.y - e.y, 2))
                    shot = sorted([s for s in wep.shots]
                                  , key=lambda k: k.calc_shot_chance(wep.range, dist, p.accuracy)
                                  , reverse=True)[0]
                    hit = wep.shoot(shot, dist, p.accuracy)
                    print(rnd, p.id, e.id, e.health, hit)
                    if hit:
                        e.health -= min([hit, e.health])

                    self.log.append("|".join([str(rnd), str(p.id), str(e.id), str(hit), str(e.health)]))
                    p.time_units -= shot.cost
                    p.timeout = shot.calc_shot_timeout(p.speed)

            [pl.Crew.remove(a) for a in pl.Crew if not a.health]
            [self.Crew.remove(b) for b in self.Crew if not b.health]
            [all_p.remove(p) for p in all_p if not p.health]

            for p in all_p:
                p.time_units += p.TUps * next_timeout

            rnd += 1
            yield next_timeout

    def despawn(self):
        self.spawn_event = None
        self.sector.remove_object(self.map_object)
        SharedData().remove_ufo(self.id)
        # del SharedData.AllFlyingObjects[self.id]
        pass

    @gen.coroutine
    def start_battle(self, p: Player):
        self.Crew = [Sectoid("Enemy {}".format(i))
                     for i in range(random.randint(self.data["min_enemies"], self.data["max_enemies"]))]
        i = 0
        for turn in self.battle_loop(p):
            # if turn != 1:
            yield gen.sleep(turn)
            if i != len(self.log):
                AWaiters().deliver(
                    AWaiters.WAIT_FOR_BATTLE_EVENTS,
                    str(self.log[i:])
                )
                i = len(self.log)

        AWaiters().deliver(AWaiters.WAIT_FOR_BATTLE_EVENTS, "Done.")
        self.spawn_event.ticks = 0
