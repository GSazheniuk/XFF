import json
import random

import config

from BaseMapObject import BaseMapObject


class Player(BaseMapObject):
    def __init__(self, name, last_name, organization, token, sector):
        BaseMapObject.__init__(self, random.randint(0, 99999), random.randint(0, 99999), 1, config.MapObjectTypes.PLAYER)
        self.Name = '%s %s' % (name, last_name)
        self.Organization = organization
        self.Token = token
        self.CurrentSector = sector
        self.Attributes = dict()
        self.Attributes['Willpower'] = 20
        self.Attributes['Intellect'] = 20
        self.Attributes['Memory'] = 20
        self.Attributes['Perception'] = 20
        self.Attributes['Endurance'] = 20
        pass

    def toJSON(self):
        res = '{'
        res += '"Name": "%s"' % self.Name
        res += ', "Token": "%s"' % self.Token
        res += ', "Sector": "%s"' % self.CurrentSector.get_id()
        res += ', "Attributes": %s' % json.dumps(self.Attributes)
        res += ', "Organization": %s' % self.Organization.toJSON()
        res += '}'
        return res
