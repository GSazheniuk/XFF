import json
import config


class Skill:
    def __init__(self, name, cost, reqs):
        self.Name = name
        self.Cost = cost
        self.Reqs = reqs
        self.Level = 0
        self.Progress = 0
        self.Status = config.SkillStatuses.SKILL_AVAILABLE if len(reqs) == 0 else config.SkillStatuses.SKILL_UNAVAILABLE
        pass


class BaseSkills:
    def __init__(self):
        self._id = 1
        self.GroupName = 'Base Maintenance'
        self.Skills = []
        self.Skills.append(Skill('Construction', 300, []))
        self.Skills.append(Skill('Advanced Construction', 500, {'Construction': 2}))
        pass

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


class TechSkills:
    def __init__(self):
        self._id = 2
        self.GroupName = 'Research'
        self.Skills = []
        self.Skills.append(Skill('Basic Research', 300, []))
        self.Skills.append(Skill('Advanced Research', 500, {'Basic Research': 2}))
        pass

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)
