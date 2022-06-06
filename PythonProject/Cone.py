from math import sin, cos, tan, radians, degrees, atan
import glm

from Point import Point
from Line import Line

class Cone:

    center: Point
    theta: float
    mew: float
    delta: float

    def __init__(self, center: Point, theta: float, mew: float):
        self.center = center
        self.theta = theta
        self.mew = mew
        self.delta = (180 - theta) / 2

    def get_triangle_vertices(self, scale: float, base_vector: glm.vec3) -> list[Point]:
        bottom_vector = glm.vec3(base_vector)  # Apparently needed for PyGLM/Python in general
        bottom_vector.y = 0
        bottom_vector = glm.normalize(bottom_vector)
        if bottom_vector.x < 0:
            bottom_vector *= -1

        opposite = scale / 2
        height = opposite / tan(radians(self.theta / 2))
        bottom_center = glm.vec3(self.center.x,
                                 self.center.y - height + self.mew * height,
                                 self.center.z)

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

    scale: float
    topCone: Cone
    bottomCone: Cone
    collision_point: Point
    vector_between: glm.vec3
    topCollision: bool

    # Those need to be a complex curve in 3D, possible evaluated only at a "marching step"
    collision_direction_1: glm.vec3 = glm.vec3(0,0,0)
    collision_direction_2: glm.vec3 = glm.vec3(0,0,0)

    def __init__(self, c1: Cone, c2: Cone):

        self.topCone = max(c1, c2, key=lambda c: c.center.y)
        self.bottomCone = min(c1, c2, key=lambda c: c.center.y)
        yDiff = self.topCone.center.y - self.bottomCone.center.y
        xzDiff = glm.length(glm.vec2(self.topCone.center.x - self.bottomCone.center.x,
                                     self.topCone.center.z - self.bottomCone.center.z))
        if yDiff != 0:
            angle = degrees(atan(xzDiff/yDiff))
        else:  # This shouldn't happen
            angle = 90
        self.topCollision = c1.theta / 2 > angle

        self.scale = c1.calc_scale(c2.center, self.topCollision)
        self.vector_between = c1.center.vectorFromTo(c2.center)

        if self.topCollision:
            self.collision_point = self.bottomCone.get_triangle_vertices(self.scale, self.vector_between)[0]
        else:  # TODO: idk if this works in 3D
            if self.topCone.center.x > self.bottomCone.center.x:
                self.collision_point = self.topCone.get_triangle_vertices(self.scale, self.vector_between)[1]
            else:
                self.collision_point = self.topCone.get_triangle_vertices(self.scale, self.vector_between)[2]

    def calculate_directions(self):
        topConeTriangle = self.topCone.get_triangle_vertices(self.scale + 1, self.vector_between)
        bottomConeTriangle = self.bottomCone.get_triangle_vertices(self.scale + 1, self.vector_between)

        topConeBase = Line(topConeTriangle[1], end=topConeTriangle[2])

        if self.topCollision:  # In 3D an expanding cone from collision in direction (0, -1, 0)
            bottomConeLeft = Line(bottomConeTriangle[0], end=bottomConeTriangle[1])
            bottomConeRight = Line(bottomConeTriangle[0], end=bottomConeTriangle[2])
            intersection_1 = topConeBase.findIntersection2D(bottomConeLeft)
            intersection_2 = topConeBase.findIntersection2D(bottomConeRight)

        else:  # In 3D an elliptical-sphere like surface, maybe a sideways cone
            if self.topCone.center.x > self.bottomCone.center.x:
                bottomConeRight = Line(bottomConeTriangle[0], end=bottomConeTriangle[2])
                topConeLeft = Line(topConeTriangle[0], end=topConeTriangle[1])
                intersection_1 = bottomConeRight.findIntersection2D(topConeLeft)
                intersection_2 = bottomConeRight.findIntersection2D(topConeBase)
            else:
                bottomConeLeft = Line(bottomConeTriangle[0], end=bottomConeTriangle[1])
                topConeRight = Line(topConeTriangle[0], end=topConeTriangle[2])
                intersection_1 = bottomConeLeft.findIntersection2D(topConeRight)
                intersection_2 = bottomConeLeft.findIntersection2D(topConeBase)

        self.collision_direction_1 = glm.normalize(self.collision_point.vectorFromTo(intersection_1))
        self.collision_direction_2 = glm.normalize(self.collision_point.vectorFromTo(intersection_2))

