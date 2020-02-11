import json


class BaseSite:
    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


class BasicSectoidOperation(BaseSite):
    def __init__(self):
        self._id = 0
        self.site_type = "Basic Sectoid Operation"
        self.min_enemies = 3
        self.max_enemies = 5
        self.encounter_types = ["Sectoid"]
        self.probability = 25000
        pass

    def get_id(self):
        return self._id
