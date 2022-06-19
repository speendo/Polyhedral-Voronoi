import glm

class Point:
    x: float
    y: float
    z: float
    id: int

    def __init__(self, coords: glm.vec3, id_number: int = None):
        self.id = id_number
        self.coords = coords
        self.x = coords.x
        self.y = coords.y
        self.z = coords.z

    def euclidean_distance(self, other_point: 'Point') -> float:
        return glm.distance(self.coords, other_point.coords)

    def vectorFromTo(self, other_point: 'Point') -> glm.vec3:
        return glm.vec3(
            round(other_point.x - self.x, 2),
            round(other_point.y - self.y, 2),
            round(other_point.z - self.z, 2)
        )

