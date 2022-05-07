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


class Points:
    def __init__(self, number_of_points, max_x, max_y, max_z):
        self.points = np.empty(number_of_points, dtype=Point)
        self.max_x = max_x
        self.max_y = max_y
        self.max_z = max_z

    def set_random(self):
        for i in range(self.points.size):
            self.points[i] = Point(x=np.random.uniform(0, self.max_x), y=np.random.uniform(0, self.max_y),
                                   z=np.random.uniform(0, self.max_z), id_number=i)

    def get(self):
        return self.points
