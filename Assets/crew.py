import random
from Assets.weapons import Rifle
from Geoscape.BaseObjects import BaseObject


max_attr_value = 10


class Soldier(BaseObject):
    def __init__(self):
        self.id = None
        self.agility = random.randint(1, max_attr_value)
        self.strength = random.randint(1, max_attr_value)
        self.stamina = random.randint(1, max_attr_value)
        self.reaction = random.randint(1, max_attr_value)
        self.perception = random.randint(1, max_attr_value)
        self.max_time_units = self.agility*2+self.stamina
        self.max_health = self.strength*2+self.stamina
        self.time_units = self.max_time_units
        self.health = self.max_health
        self.accuracy = self.perception*2+self.reaction
        self.fov = self.perception
        self.x = None
        self.y = None
        self.right_arm = Rifle(self.time_units)
        self.name = "Rookie Soldier"
        pass


class Sectoid(BaseObject):
    def __init__(self):
        self.id = None
        self.agility = random.randint(1, max_attr_value)
        self.strength = random.randint(1, max_attr_value)
        self.stamina = random.randint(1, max_attr_value)
        self.reaction = random.randint(1, max_attr_value)
        self.perception = random.randint(1, max_attr_value)
        self.max_time_units = self.agility*2+self.stamina
        self.max_health = self.strength*2+self.stamina
        self.time_units = self.max_time_units
        self.health = self.max_health
        self.accuracy = self.perception*2+self.reaction
        self.fov = self.perception
        self.x = None
        self.y = None
        self.right_arm = Rifle(self.time_units)
        self.name = "Rookie Sectoid"
        pass
