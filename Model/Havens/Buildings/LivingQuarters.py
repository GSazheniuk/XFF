from Model.BaseClasses.BaseBuilding import BaseBuilding


class SmallApartmentsUnit(BaseBuilding):
    def new(self, haven, coos):
        super().new(
            name="Small Apartments Unit",
            type="SmallApartmentsUnit",
            haven_id=haven.id,
            coos=coos,
            power_usage=1,
            required_space=1,
            condition=100,
            maintenance_req=2,
            living_space=10
        )
