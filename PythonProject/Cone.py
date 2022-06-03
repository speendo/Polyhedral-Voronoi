from math import tan, radians, degrees, atan, sin
from typing import final

import numpy as np
import glm

from Point import Point


class Cone:

    CENTER: Point
    THETA: float
    MEW: float
    DELTA: float

    def __init__(self, center: Point, theta: float, mew: float):
        self.CENTER: final = center
        self.THETA: final = theta
        self.MEW: final = mew
        self.DELTA: final = (180 - theta) / 2
        self.base_height = 1 / 2 / tan(radians(theta / 2))

    def get_triangle_vertices(self, scale: float, bottom_vector: glm.vec3) -> list[Point]:
        bottom_vector.y = 0
        bottom_vector = glm.normalize(bottom_vector)
        if bottom_vector.x < 0:
            bottom_vector *= -1

        opposite = scale / 2
        height = opposite / tan(radians(self.THETA / 2))
        bottom_center = glm.vec3(self.CENTER.x, self.CENTER.y - height + self.MEW * height, self.CENTER.z)

        # Points are returned (Top Point, Left Point, Right Point) of triangle
        return [Point(glm.vec3(self.CENTER.x, bottom_center.y + height, self.CENTER.z)),
                Point(bottom_center - bottom_vector * opposite),
                Point(bottom_center + bottom_vector * opposite)]

    # TODO: Rewrite for 3D
    def calc_scale(self, point: Point, top: bool) -> float:
        if top:
            return (point.y - self.CENTER.y) / (1 / 2 / tan(radians(self.THETA / 2)))
        dist = self.CENTER.euclidean_distance(point)
        alpha = degrees(atan(abs((point.y - self.CENTER.y) / (point.x - self.CENTER.x))))
        return dist * sin(radians(180 - alpha - self.DELTA)) / sin(radians(self.DELTA))


class Distance:

    scale: float
    c1: Cone
    c2: Cone

    def __init__(self, c1: Cone, c2: Cone):
        self.c1: final = c1
        self.c2: final = c2

        topcone = max(c1, c2, key=lambda c: c.CENTER.y)
        bottomcone = min(c1, c2, key=lambda c: c.CENTER.y)
        ydiff = topcone.CENTER.y - bottomcone.CENTER.y
        xzdiff = glm.length(glm.vec2(topcone.CENTER.x - bottomcone.CENTER.x, topcone.CENTER.z - bottomcone.CENTER.z))
        angle = degrees(atan(xzdiff/ydiff))

        print(c1.THETA/2 > angle)

        self.scale: final = c1.calc_scale(c2.CENTER, c1.THETA/2 > angle)
