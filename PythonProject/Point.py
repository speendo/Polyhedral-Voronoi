from typing import final

import numpy as np
import glm

class Point:
    x: float
    y: float
    z: float
    id: int

    def __init__(self, coords: glm.vec3, id_number: int = None):
        self.id: final = id_number
        self.coords: final = coords
        self.x: final = coords.x
        self.y: final = coords.y
        self.z: final = coords.z

    def euclidean_distance(self, other_point: 'Point') -> float:
        return glm.distance(self.coords, other_point.coords)

    def vectorBetween(self, other_point: 'Point') -> glm.vec3:
        return glm.vec3(other_point.x - self.x, other_point.y - self.y, other_point.z - self.z)
