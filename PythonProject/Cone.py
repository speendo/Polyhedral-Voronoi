import math
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

    def point_inside_cone(self, point: Point, scale: float) -> bool:
        # https://math.stackexchange.com/a/1915286/1049475
        # This needs to be expanded if we ever have cones with axis different to (0,1,0)
        cone_triangle = self.get_triangle_vertices(scale, glm.vec3(1, 0, 0))
        cone_tip = cone_triangle[0]
        cone_base = glm.vec3(cone_tip.x, cone_triangle[1].y, cone_tip.z)
        if not cone_base.y < point.y < cone_tip.y:
            return False
        h = cone_tip.y - cone_triangle[1].y
        r = cone_tip.x - cone_triangle[1].x
        point_distance = (point.x - cone_base.x) ** 2 + (point.z - cone_base.z) ** 2
        return point_distance <= ((point.y - cone_base.y - h) ** 2) * (r**2/h**2)

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


