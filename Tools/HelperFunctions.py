def minimum(a, b):
    if a < b:
        return a
    return b


def distance(aX, aY, bX, bY):
    return round(((bX - aX)**2 + (bY - aY)**2)**(1/2.0))
