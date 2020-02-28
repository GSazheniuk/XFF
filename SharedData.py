from Model.MongoCollections import UFOs, GroundSite
from Logger import Logger
from Chat import Chat
from map import Map
from Geoscape.GeoLoop import GeoLoop
from Tools import mongohelper

import config


print("Shared Data imported....")
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

m_helper = mongohelper.MongoHelper()
# Populate UFOs collection with default objects
if config.BACKSERVER_POPULATE_MONGO:
    m_helper.add_ufo(UFOs.Probe())
    m_helper.add_ufo(UFOs.SmallScout())
    m_helper.add_ufo(UFOs.MediumScout())
    m_helper.add_ufo(UFOs.LargeScout())
    m_helper.add_site(GroundSite.BasicSectoidOperation())

# Load Collections from Mongo
all_ufos = m_helper.get_all_ufos()
all_sites = m_helper.get__all_sites()


def get_current_player(req):
    token_id = 0
    res = []
    session_id = req.get_cookie('sessionId')

    if session_id in OnlinePlayers:
        token_id = OnlinePlayers[session_id]

    if token_id in Players:
        return Players[token_id]

    return res
