import HelperFunctions
import config


def approach_to_object(**kwargs):
    obj = None
    player = None
    if "player" in kwargs:
        player = kwargs["player"]
    if "object" in kwargs:
        obj = kwargs["object"]

    if player is None or obj is None:
        print("approach_to_object error: player or object is None!")
        return 0

    aircraft = player.Aircraft
    pmo = player.MapObject
    mo = obj.map_object
#    o_speed = obj.data["speed"]

    if aircraft["speed"] < aircraft["max_speed"]:
        aircraft["speed"] = HelperFunctions.minimum(aircraft["speed"] + aircraft["acceleration"], aircraft["max_speed"])

    dist = HelperFunctions.distance(pmo.X, pmo.Y, mo.X, mo.Y)
    print('Distance to object: ', dist)
    k = aircraft["speed"] / dist
    pmo.X += round((mo.X-pmo.X)*k)
    pmo.Y += round((mo.Y-pmo.Y)*k)
    if dist <= aircraft["speed"]:
        player.Status = config.PlayerStatuses.PLAYER_STATUS_MOVING
        return 1

    return 0
