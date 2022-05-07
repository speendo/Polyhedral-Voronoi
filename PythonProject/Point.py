import numpy as np


class Point:

    def __init__(self, id: int, x: float, y: float, z: float):
        self.id = id
        self.coords = np.array([x, y, z])

    def x(self) -> float:
        return self.coords[0]

    def y(self) -> float:
        return self.coords[1]

    def z(self) -> float:
        return self.coords[2]

    def euclidean_distance(self, other_point: 'Point') -> float:
        return np.linalg.norm(self.coords - other_point.coords)


class Points:
    def __init__(self, number_of_points, max_x, max_y, max_z):
        self.Points = np.empty(number_of_points, dtype=Point)
        self.max_x = max_x
        self.max_y = max_y
        self.max_z = max_z

    def set_random(self):
        [Point(np.random.uniform(0, self.max_x), np.random.uniform(0, self.max_y), np.random.uniform(0, self.max_z))
         for _ in range(self.Points.size)]

    def get(self):
        return self.Points
