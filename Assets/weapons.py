import random

from Model.BaseClasses.BaseObjects import BaseObject


class Shot(BaseObject):
    def __init__(self, name, cost, acc_mod, dmg_mod, rng_mod, speed):
        self.name = name
        self.cost = cost if cost > 0 else 1
        self.acc_mod = acc_mod
        self.dmg_mod = dmg_mod
        self.rng_mod = rng_mod
        self.speed = speed

    def calc_shot_chance(self, wep_rng, tgt_rng, acc):
        return 0.95*min([1, (wep_rng+self.rng_mod + acc*self.acc_mod/3)/(max([tgt_rng*2 - wep_rng, tgt_rng]))])

    def calc_shot_timeout(self, speed):
        return self.speed / speed


class SnapShot(Shot):
    def __init__(self, total_tus):
        super().__init__("Snap shot", round(0.25*total_tus), 0.66, 1, 0, 3)
        pass


class Weapon(BaseObject):
    def __init__(self, rng, damage, shots):
        self.range = rng
        self.damage = damage
        self.shots = shots
        pass

    def shoot(self, shot, tgt_rng, acc):
        if random.random() <= shot.calc_shot_chance(self.range, tgt_rng, acc):
            return random.randint(0, self.damage)
        else:
            return None
        pass


class Rifle(Weapon):
    def __init__(self, total_tus):
        super().__init__(7, 3, [SnapShot(total_tus)])
        pass