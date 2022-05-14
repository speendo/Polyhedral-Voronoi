from math import tan, radians, degrees, atan, sin
from typing import final

import numpy as np

from Line2D import Line2D
from Point import Point, Points


class Collision:
    def __init__(self, point: Point, scale: float, triangle: 'Triangle', has_happened: bool = False):
        self.point = point
        self.scale = scale
        self.triangle = triangle
        self.has_happened = has_happened
        self.line1 = None
        self.line2 = None

    def collide(self):
        self.has_happened = True

    def get_scale(self) -> float:
        if self.has_happened:
            return float('inf')
        else:
            return self.scale


class TopCollision(Collision):
    def __init__(self, point: Point, scale: float, triangle: 'Triangle', max_x: float, min_x: float = 0,
                 min_y: float = 0, has_happened: bool = False):
        super().__init__(point, scale, triangle, has_happened)
        self.line1 = self.generate_line("left", min_x, min_y, max_x)
        self.line2 = self.generate_line("right", min_x, min_y, max_x)

    def generate_line(self, side: str, min_x: float, min_y: float, max_x: float):
        if side == "left":
            line = Line2D(point=self.point, slope=self.triangle.left_line.slope / 2)
            line.end_point = max([line.point_at_x(min_y), line.point_at_y(min_x)], key=lambda p: p.y())
            return line
        elif side == "right":
            line = Line2D(point=self.point, slope=self.triangle.right_line.slope / 2)
            line.end_point = max([line.point_at_x(min_y), line.point_at_y(max_x)], key=lambda p: p.y())
            return line


class LeftCollision(Collision):
    def __init__(self, point: Point, scale: float, triangle: 'Triangle', max_y: float, min_x: float = 0,
                 min_y: float = 0, has_happened: bool = False):
        super().__init__(point, scale, triangle, has_happened)
        self.line1 = self.generate_vertical_line(max_y)
        self.line2 = self.generate_left_line(min_x, min_y)

    def generate_vertical_line(self, max_y):
        return Line2D(point=self.point, end_point=Point(self.point.x(), max_y, 0))

    def generate_left_line(self, min_x, min_y):
        line = Line2D(point=self.point, slope=self.triangle.left_line.slope / 2)
        line.end_point = max([line.point_at_x(min_y), line.point_at_y(min_x)], key=lambda p: p.y)
        return line


class RightCollision(Collision):
    def __init__(self, point: Point, scale: float, triangle: 'Triangle', max_x: float, max_y: float, min_y: float = 0,
                 has_happened: bool = False):
        super().__init__(point, scale, triangle, has_happened)
        self.line1 = self.generate_vertical_line(max_y)
        self.line2 = self.generate_right_line(max_x, min_y)

    def generate_vertical_line(self, max_y):
        return Line2D(point=self.point, end_point=Point(self.point.x(), max_y, 0))

    def generate_right_line(self, max_x, min_y):
        line = Line2D(point=self.point, slope=self.triangle.right_line.slope / 2)
        line.end_point = max([line.point_at_x(min_y), line.point_at_y(max_x)], key=lambda p: p.y)
        return line


def get_triangle_vertices(p: Point, mew: float, theta: float, scale: float = 1) -> list[Point]:
    opposite = scale / 2
    height = opposite / tan(radians(theta / 2))

    # Points are returned (Top Point, Left Point, Right Point) of triangle
    return [Point(p.x(), p.y() + mew * height, p.z()),
            Point(p.x() - opposite, p.y() - height + mew * height, p.z()),
            Point(p.x() + opposite, p.y() - height + mew * height, p.z())]


class Triangle:
    THETA: final = 30
    MEW: final = 0.5
    DELTA: final = (180 - THETA) / 2

    base_height = 1 / 2 / tan(radians(THETA / 2))

    origin_triangle = get_triangle_vertices(p=Point(0, 0, 0), mew=MEW, theta=THETA)
    base_line = Line2D(origin_triangle[1], end_point=origin_triangle[2])
    left_line = Line2D(origin_triangle[1], end_point=origin_triangle[0])
    right_line = Line2D(origin_triangle[2], end_point=origin_triangle[0])

    def __init__(self, center: Point):
        self.center = center

        self.hor_line = Line2D(center, slope=Triangle.base_line.slope)
        self.left_line = Line2D(center, slope=Triangle.left_line.slope)
        self.right_line = Line2D(center, slope=Triangle.right_line.slope)

        self.top_points = None
        self.left_points = None
        self.right_points = None

        self.top_collision: Collision = None
        self.right_collision: Collision = None
        self.left_collision: Collision = None

    def get_scaled_points(self, scale: float) -> list[Point]:
        return get_triangle_vertices(p=self.center, mew=self.MEW, theta=self.THETA, scale=scale)

    def categorize_points(self, points: Points):
        self.top_points = []
        self.left_points = []
        self.right_points = []

        for p in points:
            if p.id() is not self.center.id():
                if p.y() > self.center.y():
                    if self.left_line.point_position(p) >= 0 and self.right_line.point_position(p) >= 0:
                        self.top_points.append(p)
                else:
                    if self.left_line.point_position(p) >= 0:
                        self.left_points.append(p)
                    elif self.right_line.point_position(p) >= 0:
                        self.right_points.append(p)

    def calc_side_scale(self, point: Point) -> float:
        dist = self.center.euclidean_distance(point)
        alpha = degrees(atan(abs(point.y() - self.center.y()) / abs(point.x() - self.center.x())))
        return dist * sin(radians(180 - alpha - Triangle.DELTA)) / sin(radians(Triangle.DELTA))

    def calc_top_scale(self, point: Point) -> float:
        return (point.y() - self.center.y()) / Triangle.base_height

    def store_top_collision(self):
        if not self.top_points:
            # ToDo: handle no collisions
            self.top_collision = Collision(point=None, scale=float('inf'), triangle=self, has_happened=True)
        else:
            top_collision_point = min(self.top_points, key=lambda p: p.y())
            top_scale_to_hit = self.calc_top_scale(top_collision_point)
            self.top_collision = TopCollision(point=top_collision_point, scale=top_scale_to_hit, triangle=self)

    def store_left_collision(self):
        if not self.left_points:
            # ToDo: handle no collisions
            self.left_collision = Collision(point=None, scale=float('inf'), triangle=self, has_happened=True)
        else:
            self.left_collision = Collision(point=None, scale=float('inf'), triangle=self)
            for p in self.left_points:
                cur_scale = self.calc_side_scale(p)
                if cur_scale < self.left_collision.scale:
                    self.left_collision = LeftCollision(point=p, scale=cur_scale, triangle=self)

    def store_right_collision(self):
        if not self.right_points:
            # ToDo: handle no collisions
            self.right_collision = Collision(point=None, scale=float('inf'), triangle=self, has_happened=True)
        else:
            self.right_collision = Collision(point=None, scale=float('inf'), triangle=self)
            for p in self.right_points:
                cur_scale = self.calc_side_scale(p)
                if cur_scale < self.right_collision.scale:
                    self.right_collision = RightCollision(point=p, scale=cur_scale, triangle=self)

    def store_collisions(self):
        self.store_top_collision()
        self.store_left_collision()
        self.store_right_collision()

    def has_next_collision(self) -> bool:
        if (not self.top_collision.has_happened or
                not self.left_collision.has_happened or not self.right_collision.has_happened):
            return True
        else:
            return False

    def find_next_collision(self) -> Collision:
        cols = [self.top_collision, self.left_collision, self.right_collision]
        return min((c for c in cols if c is not None), key=lambda c: c.get_scale())


class Triangles:
    def __init__(self, points: Points):
        self.triangles = np.empty(points.get().size, dtype=Triangle)
        for i, p in zip(range(points.get().size), points.get()):
            self.triangles[i] = Triangle(p)
            self.triangles[i].categorize_points(points.get())
            self.triangles[i].store_collisions()

    def get(self):
        return self.triangles

    def has_next_collision(self) -> bool:
        for t in self.triangles:
            if t.has_next_collision():
                return True
        return False

    def find_next_collision(self) -> Collision:
        return min(self.triangles, key=lambda t: t.find_next_collision().get_scale()).find_next_collision()
