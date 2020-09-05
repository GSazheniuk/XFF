from Model.MongoCollections.Bunker import Bunker
from SharedData import SharedData

from Model.BaseClasses.BaseObjects import BaseObject


class Organization(BaseObject):
    def __init__(self, name):
        self.Name = name
        self.Bases = list()
        hq = Bunker(
            name="%s Headquarters" % self.Name,
            organization=self,
            sector=SharedData().get_default_sector()
        )
        self.Bases.append(hq)
        SharedData().add_base(hq)
        pass

    def toJSON2(self):
        res = '{'
        res += '"Name": "%s"' % self.Name
        res += '"Bases": "%s"' % [x.toJSON() for x in self.Bases]
        res += '}'
        return res

    def to_simple_JSON(self):
        res = '{'
        res += '"Name": "%s"' % self.Name
        res += '}'
        return res
