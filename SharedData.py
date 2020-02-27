from Logger import Logger
from Chat import Chat
from map import Map
from Geoscape.GeoLoop import GeoLoop


OnlinePlayers = {}
Players = {}
AllFlyingObjects = {}
AllBases = {}
Sessions = {}
Chat = Chat()
Map = Map(1, 1)
Log = Logger('XFF', 'SharedData')
frontServicesFree = 0
AllMapActions = {}
Queue_Skills = []
Loop = GeoLoop()


def get_current_player(req):
    token_id = 0
    res = []
    session_id = req.get_cookie('sessionId')

    if session_id in OnlinePlayers:
        token_id = OnlinePlayers[session_id]

    if token_id in Players:
        return Players[token_id]

    return res
