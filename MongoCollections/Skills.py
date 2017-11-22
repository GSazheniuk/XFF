import json
import config


class Skill:
    def __init__(self, name, cost, reqs, skill_group, prim_attr, sec_attr, _id):
        self.Name = name
        self.Cost = cost
        self.Reqs = reqs
        self.Level = 0
        self.Progress = 0
        self.SkillGroup = skill_group
        self.PrimaryAttribute = prim_attr
        self.SecondaryAttribute = sec_attr
        self.Status = config.SkillStatuses.SKILL_AVAILABLE if len(reqs) == 0 else config.SkillStatuses.SKILL_UNAVAILABLE
        self._id = _id
        pass

    def __str__(self):
        return str(self.__dict__)


def default_skills():
    skills = list()
    skills.append(Skill('Construction', 300, [], 'Base Maintenance', 'Endurance', 'Charisma', 1))
    skills.append(
        Skill('Advanced Construction', 500, [{'Construction': 2}], 'Base Maintenance', 'Endurance', 'Charisma', 2)
    )
    skills.append(Skill('Basic Research', 300, [], 'Research', 'Intellect', 'Memory', 3))
    skills.append(
        Skill('Advanced Research', 500, [{'Basic Research': 2}], 'Research', 'Intellect', 'Memory', 4)
    )
    return skills
