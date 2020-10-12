from Model.BaseClasses.BaseHaven import BaseHaven
from Model.Havens.Buildings import *
from Model.Havens.Buildings import PowerGenerators, LivingQuarters


class Headquarters(BaseHaven):
    def new(self, org, owner, point):
        super().new(
            name="%s HQs" % org.name,
            type="Headquarters",
            owner_id=owner.id,
            point=point,
            scan_rng=1500,
            atk_rng=500,
            buildings={},
            controlling_org_id=org.id,
            building_spots=[
                [0, 0, 0], [-1, 1, 0], [-1, 0, 1], [1, -1, 0], [1, 0, -1], [-2, 2, 0], [2, -2, 0],
                [[-2, 0, 2], [-2, 1, 1], [-3, 2, 1], [-3, 1, 2]],
                [[2, 0, -2], [2, -1, -1], [3, -2, -1], [3, -1, -2]],
                [[0, 1, -1], [-1, 2, -1], [0, 2, -2], [1, 1, -2]],
                [[0, -1, 1], [1, -2, 1], [0, -2, 2], [-1, -1, 2]]]
        )
        pg = PowerGenerators.SmallNuclearGenerator()
        pg.new(self)
        self.buildings[pg.id] = pg
        self.building_spots[0].append(pg.id)
        lq = LivingQuarters.SmallApartmentsUnit()
        lq.new(self, [-1, 0, 1])
        self.buildings[lq.id] = lq
        self.building_spots[2].append(pg.id)
