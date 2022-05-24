import numpy as np


class Point:
    def __init__(self, x: float, y: float, z: float, id_number: int = None):
        self.id_number = id_number
        self.coords = np.array([x, y, z])

    def x(self) -> float:
        return self.coords[0]

    def y(self) -> float:
        return self.coords[1]

    def z(self) -> float:
        return self.coords[2]

    def id(self) -> int:
        return self.id_number

    def euclidean_distance(self, other_point: 'Point') -> float:
        return np.linalg.norm(self.coords - other_point.coords)