from Model.BaseClasses.BaseHaven import BaseHaven


class Headquarters(BaseHaven):
    def new(self, org, owner, point):
        super().new(
            name="%s HQs" % org.name,
            type="Headquarters",
            owner_id=owner.id,
            point=point,
            scan_rng=1500,
            atk_rng=500,
            controlling_org_id=org.id,
            max_building_tier=5
        )
