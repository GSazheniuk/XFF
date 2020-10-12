from Model.BaseClasses.BaseBuilding import BaseBuilding


class SmallNuclearGenerator(BaseBuilding):
    def new(self, haven):
        super().new(
            name="Small Nuclear Power Source",
            type="SmallNuclearGenerator",
            haven_id=haven.id,
            coos=[[0, 0, 0]],
            power_output=15,
            required_space=1,
            condition=100,
            maintenance_req=1
        )
