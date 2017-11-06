import config
import random
import MapActions

from Logger import Logger
from Chat import Chat
from map import Map


OnlinePlayers = {}
Players = {}
AllFlyingObjects = {}
Sessions = {}
Chat = Chat()
Map = Map(1, 1)
Log = Logger('XFF', 'SharedData')
frontServicesFree = 0
AllMapActions = {}


def get_current_player(req):
    token_id = 0
    res = []
    session_id = req.get_cookie('sessionId')

    if session_id in OnlinePlayers:
        token_id = OnlinePlayers[session_id]

    if token_id in Players:
        return Players[token_id]

    return res


def add_map_action(player, ufo, action_type):
    if action_type == config.MapActionTypes.ACTION_TYPE_APPROACH:
        AllMapActions[str(random.randint(0, 1000000))] = {
            "action": MapActions.approach_to_object,
            "kwargs": {
                "player": player,
                "object": ufo,
            }
        }
    elif action_type == config.MapActionTypes.ACTION_TYPE_APPEAR:
        ufo.duration = ufo.data["actions"][action_type]["max_duration"]
        AllMapActions[str(random.randint(0, 1000000))] = {
            "action": MapActions.appear,
            "kwargs": {
                "object": ufo,
            }
        }
    elif action_type == config.MapActionTypes.ACTION_TYPE_MOVE_TO_POINT:
        ufo.duration = ufo.data["actions"][action_type]["max_duration"]
        AllMapActions[str(random.randint(0, 1000000))] = {
            "action": MapActions.move_to_point,
            "kwargs": {
                "object": ufo,
                "point": {
                    "X": random.randint(0, config.MAP_DEFAULT_SECTOR_WIDTH),
                    "Y": random.randint(0, config.MAP_DEFAULT_SECTOR_HEIGHT),
                }
            }
        }
    elif action_type == config.MapActionTypes.ACTION_TYPE_LEAVE:
        ufo.duration = ufo.data["actions"][action_type]["max_duration"]
        AllMapActions[str(random.randint(0, 1000000))] = {
            "action": MapActions.disappear,
            "kwargs": {
                "object": ufo,
            }
        }

    pass
