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


def move_to_point(**kwargs):
    obj = None
    point = None

    if "object" in kwargs:
        obj = kwargs["object"]
    if "point" in kwargs:
        point = kwargs["point"]

    if point is None or obj is None:
        print("move_to_point error: point or object is None!")
        return 0

    mo = obj.map_object
    o = obj.data

    if "speed" not in o:
        o["speed"] = 0

    if o["speed"] < o["max_speed"]:
        o["speed"] = HelperFunctions.minimum(o["speed"] + o["acceleration"], o["max_speed"])

    dist = HelperFunctions.distance(mo.X, mo.Y, point["X"], point["Y"])
    print('Distance to point: ', dist)
    k = o["speed"] / dist
    mo.X += round((point["X"]-mo.X)*k)
    mo.Y += round((point["Y"]-mo.Y)*k)
    obj.duration -= 1

    if dist <= o["speed"] or obj.duration == 0:
        # obj.Status = config.UfoStatuses.UFO_STATUS_MOVING
        # obj.map_object.status = config.UfoStatuses.UFO_STATUS_MOVING
        return 1

    obj.map_object.status = config.UfoStatuses.UFO_STATUS_MOVING
    print(obj.id, ' moving for next ', obj.duration, ' ticks')
    return 0


def appear(**kwargs):
    obj = None

    if "object" in kwargs:
        obj = kwargs["object"]

    if obj is None:
        print('appear error: object is None!')
        return 0

    obj.duration -= 1

    if obj.duration == 0:
        obj.Status = config.PlayerStatuses.PLAYER_STATUS_MOVING
        return 1

    obj.map_object.status = config.UfoStatuses.UFO_STATUS_APPEARING
    print(obj.id, ' appears in ', obj.duration, ' ticks')
    return 0


def disappear(**kwargs):
    obj = None

    if "object" in kwargs:
        obj = kwargs["object"]

    if obj is None:
        print('disappear error: object is None!')
        return 0

    obj.duration -= 1

    if obj.duration == 0:
        obj.Status = config.PlayerStatuses.PLAYER_STATUS_MOVING
        return -1

    obj.map_object.status = config.UfoStatuses.UFO_STATUS_LEAVING
    print(obj.id, ' leaves in ', obj.duration, ' ticks')
    return 0
