from Bunker import Bunker
import SharedData


class Organization:
    def __init__(self, name):
        self.Name = name
        self.Bases = []
        hq = Bunker(
            name="%s Headquarters" % self.Name,
            organization=self,
            sector=SharedData.Map.DefaultSector
        )
        self.Bases.append(hq)
        SharedData.AllBases[hq.get_id()] = hq
        pass

    def toJSON(self):
        res = '{'
        res += '"Name": "%s"' % self.Name
        res += '}'
        return res
