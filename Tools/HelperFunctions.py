from pygeodesy import ellipsoidalVincenty
from map import Point
import requests


GEOLOCATION_URL = "http://api.geonames.org/extendedFindNearbyJSON?lat=%s&lng=%s&username=MrRandomizer"

def minimum(a, b):
    if a < b:
        return a
    return b


def distance(aX, aY, bX, bY):
    return round(((bX - aX)**2 + (bY - aY)**2)**(1/2.0))


def distance2(pointA, pointB):
    start_point = ellipsoidalVincenty.LatLon(pointA.Lat, pointA.Long)
    end_point = ellipsoidalVincenty.LatLon(pointB.Lat, pointB.Long)
    return start_point.distanceTo(end_point)/1000


def next_point(pointA, pointB, speed):
    start_point = ellipsoidalVincenty.LatLon(pointA.Lat, pointA.Long)
    end_point = ellipsoidalVincenty.LatLon(pointB.Lat, pointB.Long)
    new_point = start_point.destination(speed, start_point.initialBearingTo(end_point))
    return Point(new_point.lat, new_point.lon)


def get_location_name(point: Point):
    req = requests.get(GEOLOCATION_URL % (point.Lat, point.Long))
    res = req.json()
    print(res)
    if "ocean" in res:
        return res["ocean"]["name"]

    if "continent" in res:
        return res["countryName"]

    if "geonames" in res:
        res = res["geonames"][-1]

    name = ""
    if "city" in res["fclName"]:
        name = res["name"]
        if "countryName" in res["fclName"]:
            name += ", %s" % res["countryName"]
    return name
