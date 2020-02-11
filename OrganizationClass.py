from MongoCollections.Bunker import Bunker
import SharedData

from BaseMapObject import BaseObject


class Organization(BaseObject):
    def __init__(self, name):
        self.Name = name
        self.Bases = list()
        hq = Bunker(
            name="%s Headquarters" % self.Name,
            organization=self,
            sector=SharedData.Map.DefaultSector
        )
        self.Bases.append(hq)
        SharedData.AllBases[hq.get_id()] = hq
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
