from math import tan, radians
from typing import final

import numpy as np
import glm

from Point import Point


class Cone:

    def __init__(self, center: Point, theta: float, mew: float):
        self.CENTER: final = center
        self.THETA: final = theta
        self.MEW: final = mew
        self.DELTA: final = (180 - theta) / 2

    def get_triangle_vertices(self, scale: float, bottom_vector: glm.vec3) -> list[Point]:
        bottom_vector.y = 0
        bottom_vector = glm.normalize(bottom_vector)
        if bottom_vector.z < 0:
            bottom_vector *= -1
        opposite = scale / 2
        height = opposite / tan(radians(self.THETA / 2))
        bottom_center = glm.vec3(self.CENTER.x, self.CENTER.y - height + self.MEW * height, self.CENTER.z)

        # Points are returned (Top Point, Left Point, Right Point) of triangle
        return [Point(glm.vec3(self.CENTER.x, bottom_center.y + height, self.CENTER.z)),
                Point(bottom_center - bottom_vector * opposite),
                Point(bottom_center + bottom_vector * opposite)]

        """
                Point(self.CENTER.x - opposite, self.CENTER.y - height + self.MEW * height, self.CENTER.z),
                Point(self.CENTER.x + opposite, self.CENTER.y - height + self.MEW * height, self.CENTER.z)]
        """