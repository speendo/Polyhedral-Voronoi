from math import sqrt

class Point:
    x: float
    y: float
    z: float

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z




def pointdistance(p1: Point, p2: Point):
    xdiff = p1.x-p2.x
    ydiff = p1.y-p2.y
    zdiff = p1.z-p2.z
    return sqrt(xdiff * xdiff + ydiff * ydiff + zdiff * zdiff)
