import random
from Assets.weapons import Rifle
from Model.BaseClasses.BaseObjects import BaseObject
import config

max_attr_value = 10


class Soldier(BaseObject):
    def __init__(self, name):
        self.timeout = 0
        self.team = 0
        self.agility = random.randint(1, max_attr_value)
        self.strength = random.randint(1, max_attr_value)
        self.stamina = random.randint(1, max_attr_value)
        self.reaction = random.randint(1, max_attr_value)
        self.speed = sum([self.agility, self.reaction, self.reaction])/3
        self.perception = random.randint(1, max_attr_value)
        self.max_time_units = self.agility*2+self.stamina
        self.TUps = self.max_time_units / 60 * self.speed / max_attr_value
        self.max_health = self.strength*2+self.stamina
        self.time_units = self.max_time_units
        self.health = self.max_health
        self.accuracy = self.perception*2+self.reaction
        self.fov = self.perception
        self.x = None
        self.y = None
        self.id = random.randint(0, config.PLAYER_MAX_ID)
        self.right_arm = Rifle(self.time_units)
        self.name = name
        pass


class Sectoid(BaseObject):
    def __init__(self, name):
        self.timeout = 0
        self.team = 1
        self.agility = random.randint(1, max_attr_value)
        self.strength = random.randint(1, max_attr_value)
        self.stamina = random.randint(1, max_attr_value)
        self.reaction = random.randint(1, max_attr_value)
        self.speed = sum([self.agility, self.reaction, self.reaction])/3
        self.perception = random.randint(1, max_attr_value)
        self.max_time_units = self.agility*2+self.stamina
        self.TUps = self.max_time_units / 60 * self.speed / max_attr_value
        self.max_health = self.strength*2+self.stamina
        self.time_units = self.max_time_units
        self.health = self.max_health
        self.accuracy = self.perception*2+self.reaction
        self.fov = self.perception
        self.x = None
        self.y = None
        self.right_arm = Rifle(self.time_units)
        self.name = name
        pass
