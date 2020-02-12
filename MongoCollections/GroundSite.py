import json


class BaseSite:
    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


class BasicSectoidOperation(BaseSite):
    def __init__(self):
        self._id = 101
        self.site_type = "Basic Sectoid Operation"
        self.min_enemies = 3
        self.max_enemies = 5
        self.encounter_types = ["Sectoid"]
        self.probability = 25000
        self.actions = {
            "appear": {"probability": 0, "max_duration": 5, "status": 0},
            "stay": {"probability": 8, "max_duration": 12, "status": 1},
            "leave": {"probability": 2, "max_duration": 15, "status": 0},
        }
        pass

    def get_id(self):
        return self._id
