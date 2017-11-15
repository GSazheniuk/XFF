import json
import random

import config
import map

from BaseMapObject import BaseMapObject


class Player:
    def __init__(self, name, last_name, organization, token, sector: map.MapSector):
        self.MapObject = BaseMapObject(
            random.randint(0, config.MAP_DEFAULT_SECTOR_WIDTH),
            random.randint(0, config.MAP_DEFAULT_SECTOR_HEIGHT),
            5,
            config.MapObjectTypes.PLAYER,
            token,
        )
        self.Name = '%s %s' % (name, last_name)
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

    def toJSON(self):
        res = '{'
        res += '"Name": "%s"' % self.Name
        res += ', "Token": "%s"' % self.Token
        res += ', "Sector": "%s"' % self.CurrentSector.get_id()
        res += ', "Attributes": %s' % json.dumps(self.Attributes)
        res += ', "Organization": %s' % self.Organization.toJSON()
        res += ', "Aircraft": %s' % json.dumps(self.Aircraft)
        res += ', "MapObject": %s' % json.dumps(self.MapObject.get_dict())
        res += '}'
        return res
