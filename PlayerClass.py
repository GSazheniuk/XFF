import config
import map
from MongoCollections import Skills

from BaseMapObject import BaseMapObject, BaseObject


class Player(BaseObject):
    def __init__(self, name, last_name, organization, token, sector: map.MapSector):
        self.Name = '%s %s' % (name, last_name)
        self.MapObject = BaseMapObject(
            map.Point(),
            5,
            config.MapObjectTypes.PLAYER,
            token,
            self.Name
        )
        self.Organization = organization
        self.Token = token
        self.CurrentSector = sector
        self.Status = config.PlayerStatuses.PLAYER_STATUS_STOPPED
        self.Attributes = dict()
        self.Attributes['Willpower'] = 20
        self.Attributes['Intellect'] = 20
        self.Attributes['Memory'] = 20
        self.Attributes['Perception'] = 20
        self.Attributes['Endurance'] = 20
        self.Attributes['Charisma'] = 20

        self.Skills = Skills.default_skills()
        self.SkillsQueue = []
        self.Crew = []
        self.Wallet = 10000

        self.Aircraft = {
            "_id": 0,
            "diameter": 3,
            "ship_type": "Interceptor",
            "max_structure": 200,
            "max_armor": 200,
            "max_shields": 200,
            "max_speed": 250,
            "acceleration": 15,
            "structure": 200,
            "armor": 200,
            "shields": 200,
            "speed": 750,
            "min_damage": 10,
            "max_damage": 15,
            "accuracy": 100,
        }
        pass

    def skill_done(self, skill):
        skill.Level += 1
        skill.Cost *= 1.3
        skill.Progress = 0

        if len(skill.Reqs) == 0:
            skill.Status = config.SkillStatuses.SKILL_AVAILABLE
        else:
            skill.Status = config.SkillStatuses.SKILL_UNAVAILABLE
            pass

        self.SkillsQueue.remove(skill)
        pass

    def tick(self):
        if len(self.SkillsQueue) > 0:
            skill = self.SkillsQueue[0]
            skill.Status = config.SkillStatuses.SKILL_IN_PROGRESS
            a1, a2 = self.Attributes[skill.PrimaryAttribute], self.Attributes[skill.SecondaryAttribute]
            skill.Progress += min(a1 + a2//2, skill.Cost - skill.Progress)
            if skill.Progress >= skill.Cost:
                self.skill_done(skill)
            pass
        pass

    def add_skill_to_queue(self, skill_name):
        skills = [sk for sk in self.Skills if sk.Name == skill_name]
        if len(skills) > 0:
            skill = skills[0]
            if skill not in self.SkillsQueue and skill.Status == config.SkillStatuses.SKILL_AVAILABLE:
                self.SkillsQueue.append(skill)
                skill.Status = config.SkillStatuses.SKILL_QUEUED
            pass
        pass

    # def toJSON(self):
    #     res = '{'
    #     res += '"Name": "%s"' % self.Name
    #     res += ', "Token": "%s"' % self.Token
    #     res += ', "Sector": "%s"' % self.CurrentSector.get_id()
    #     res += ', "Attributes": %s' % json.dumps(self.Attributes)
    #     res += ', "Organization": %s' % self.Organization.toJSON()
    #     res += ', "Aircraft": %s' % json.dumps(self.Aircraft)
    #     res += ', "MapObject": %s' % self.MapObject.toJSON()
    #     res += ', "Skills": ' + json.dumps([skill.__dict__ for skill in self.Skills])
    #     res += ', "SkillsQueue": ' + json.dumps([skill.__dict__ for skill in self.SkillsQueue])
    #     res += '}'
    #     return res
