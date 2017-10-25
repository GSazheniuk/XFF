import json


class Probe:
    def __init__(self):
        self._id = 0
        self.ufo_type = 'Probe'
        self.probability = 45000
        self.duration = 50                      # Ticks
        self.max_instances_in_sector = 10
        self.diameter = 3
        self.max_speed = 100                    # MPS
        self.max_shields = 100
        self.max_armor = 100
        self.max_structure = 100
        self.min_crew = 1
        self.max_crew = 1
        self.max_crew_level = 1
        self.min_loot = 1
        self.max_loot = 3
        self.bounty = 100
        pass

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

    def get_id(self):
        return self._id


class SmallScout:
    def __init__(self):
        self._id = 1
        self.ufo_type = 'Small Scout'
        self.probability = 40000
        self.duration = 75                      # Ticks
        self.max_instances_in_sector = 10
        self.diameter = 5
        self.max_speed = 150                    # MPS
        self.max_shields = 200
        self.max_armor = 200
        self.max_structure = 200
        self.min_crew = 2
        self.max_crew = 5
        self.max_crew_level = 1
        self.min_loot = 2
        self.max_loot = 5
        self.bounty = 500
        self.attack_range = 0
        self.min_damage = 0
        self.max_damage = 0
        self.accuracy = 0
        pass

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

    def get_id(self):
        return self._id


class MediumScout:
    def __init__(self):
        self._id = 2
        self.ufo_type = 'Medium Scout'
        self.probability = 35000
        self.duration = 125                     # Ticks
        self.max_instances_in_sector = 8
        self.diameter = 7
        self.max_speed = 250                    # MPS
        self.max_shields = 250
        self.max_armor = 200
        self.max_structure = 400
        self.min_crew = 2
        self.max_crew = 5
        self.max_crew_level = 1
        self.min_loot = 2
        self.max_loot = 5
        self.bounty = 500
        self.attack_range = 50
        self.min_damage = 5
        self.max_damage = 20
        self.accuracy = 40
        pass

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

    def get_id(self):
        return self._id


class LargeScout:
    def __init__(self):
        self._id = 3
        self.ufo_type = 'Large Scout'
        self.probability = 25000
        self.duration = 100                     # Ticks
        self.max_instances_in_sector = 6
        self.diameter = 10
        self.max_speed = 300                    # MPS
        self.max_shields = 500
        self.max_armor = 500
        self.max_structure = 500
        self.min_crew = 7
        self.max_crew = 9
        self.max_crew_level = 2
        self.min_loot = 5
        self.max_loot = 9
        self.bounty = 1200
        self.attack_range = 150
        self.min_damage = 25
        self.max_damage = 40
        self.accuracy = 60
        pass

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

    def get_id(self):
        return self._id
