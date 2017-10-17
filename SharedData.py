from Logger import Logger
from Chat import Chat
from map import Map, MapSector


class DataHolder:

    OnlinePlayers = {}
    Players = {}
    Sessions = {}
    Chat = Chat()
    Map = Map(1, 1)
    Log = Logger('XFF', 'SharedData')
    frontServicesFree = 0

    def __init__(self):
        pass

    def __init__(self, req):
        self.currentPlayer = self.get_current_player(req)
        pass
    
    def get_current_player(sessionId):
        tokenId = 0
        res = []

        for p in DataHolder.OnlinePlayers:
            if p == sessionId:
                tokenId = DataHolder.OnlinePlayers[p]
                pass
            pass

        for p in DataHolder.Players:
            if p == tokenId:
                return DataHolder.Players[p]
            pass

        return res
