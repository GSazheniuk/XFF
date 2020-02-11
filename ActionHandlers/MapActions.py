from Tools import HelperFunctions
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

    pmo.point = HelperFunctions.next_point(pmo.point, mo.point, aircraft["speed"])
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
        if config.DEBUG_LEVEL >= config.DebugLevels.DEBUG_LEVEL_ERRORS_ONLY:
            print("move_to_point error: point or object is None!")
        return 0

    mo = obj.map_object
    o = obj.data

    if "speed" not in o:
        o["speed"] = 0

    if o["speed"] < o["max_speed"]:
        o["speed"] = HelperFunctions.minimum(o["speed"] + o["acceleration"], o["max_speed"])

    dist = HelperFunctions.distance2(mo.point, point)
    if config.DEBUG_LEVEL == config.DebugLevels.DEBUG_LEVEL_DETAILED:
        print('Distance to point: ', dist)
    mo.point = HelperFunctions.next_point(mo.point, point, o["speed"])
    # obj.duration -= 1

    if dist <= o["speed"]:  # or obj.duration == 0:
        obj.duration = 0
        # obj.Status = config.UfoStatuses.UFO_STATUS_MOVING
        # obj.map_object.status = config.UfoStatuses.UFO_STATUS_MOVING
        return 1

    obj.map_object.status = config.UfoStatuses.UFO_STATUS_MOVING
    if config.DEBUG_LEVEL == config.DebugLevels.DEBUG_LEVEL_DETAILED:
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
    if config.DEBUG_LEVEL == config.DebugLevels.DEBUG_LEVEL_DETAILED:
        print(obj.id, ' appears in ', obj.duration, ' ticks')
    return 0


def disappear(**kwargs):
    obj = None

    if "object" in kwargs:
        obj = kwargs["object"]

    if obj is None:
        if config.DEBUG_LEVEL >= config.DebugLevels.DEBUG_LEVEL_ERRORS_ONLY:
            print('disappear error: object is None!')
        return 0

    obj.duration -= 1

    if obj.duration == 0:
        obj.Status = config.PlayerStatuses.PLAYER_STATUS_MOVING
        return -1

    obj.map_object.status = config.UfoStatuses.UFO_STATUS_LEAVING
    if config.DEBUG_LEVEL == config.DebugLevels.DEBUG_LEVEL_DETAILED:
        print(obj.id, ' leaves in ', obj.duration, ' ticks')
    return 0
