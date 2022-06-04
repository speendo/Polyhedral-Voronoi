from math import tan, radians, degrees, atan, sin
from typing import final

import glm

from Point import Point


class Cone:

    # All are final/const
    center: Point
    theta: float
    mew: float
    delta: float

    def __init__(self, center: Point, theta: float, mew: float):
        self.center: final = center
        self.theta: final = theta
        self.mew: final = mew
        self.delta: final = (180 - theta) / 2

    def get_triangle_vertices(self, scale: float, bottom_vector: glm.vec3) -> list[Point]:
        bottom_vector.y = 0
        bottom_vector = glm.normalize(bottom_vector)
        if bottom_vector.x < 0:
            bottom_vector *= -1

        opposite = scale / 2
        height = opposite / tan(radians(self.theta / 2))
        bottom_center = glm.vec3(self.center.x, self.center.y - height + self.mew * height, self.center.z)

        # Points are returned (Top Point, Left Point, Right Point) of triangle
        return [Point(glm.vec3(self.center.x, bottom_center.y + height, self.center.z)),
                Point(bottom_center - bottom_vector * opposite),
                Point(bottom_center + bottom_vector * opposite)]

    # TODO: Rewrite for 3D
    def calc_scale(self, point: Point, top: bool) -> float:
        if top:
            return abs(point.y - self.center.y) / (1 / 2 / tan(radians(self.theta / 2)))
        dist = self.center.euclidean_distance(point)
        alpha = degrees(atan(abs((point.y - self.center.y) / (point.x - self.center.x))))
        return dist * sin(radians(180 - alpha - self.delta)) / sin(radians(self.delta))


class Collision:

    # All are final/const
    scale: float
    c1: Cone
    c2: Cone
    vector_between: glm.vec3
    collision_point: Point

    def __init__(self, c1: Cone, c2: Cone):
        self.c1: final = c1
        self.c2: final = c2

        topCone = max(c1, c2, key=lambda c: c.center.y)
        bottomCone = min(c1, c2, key=lambda c: c.center.y)
        yDiff = topCone.center.y - bottomCone.center.y
        xzDiff = glm.length(glm.vec2(topCone.center.x - bottomCone.center.x, topCone.center.z - bottomCone.center.z))
        if yDiff != 0:
            angle = degrees(atan(xzDiff/yDiff))
        else:  # This shouldn't happen
            angle = 90
        topCollision = c1.theta / 2 > angle

        self.scale: final = c1.calc_scale(c2.center, topCollision)
        self.vector_between: final = c1.center.vectorBetween(c2.center)

        if topCollision:
            self.collision_point: final = bottomCone.get_triangle_vertices(self.scale, self.vector_between)[0]
        else:  # TODO: idk if this works in 3D
            if topCone.center.x > bottomCone.center.x:
                self.collision_point: final = topCone.get_triangle_vertices(self.scale, self.vector_between)[1]
            else:
                self.collision_point: final = topCone.get_triangle_vertices(self.scale, self.vector_between)[2]


