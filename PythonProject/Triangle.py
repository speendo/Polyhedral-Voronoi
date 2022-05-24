from math import tan, radians, degrees, atan, sin
from typing import final

import numpy as np

from Line2D import Line2D
from Point import Point
from Collision import Collision, TopCollision, LeftCollision, RightCollision


class Triangle:
    THETA: final = 30
    MEW: final = 0.5
    DELTA: final = (180 - THETA) / 2

    base_height = 1 / 2 / tan(radians(THETA / 2))

    def __init__(self, center: Point):
        self.center = center
        self.origin_triangle = self.get_triangle_vertices()
        self.base_line = Line2D(self.origin_triangle[1], end_point=self.origin_triangle[2])
        self.left_line = Line2D(self.origin_triangle[1], end_point=self.origin_triangle[0])
        self.right_line = Line2D(self.origin_triangle[2], end_point=self.origin_triangle[0])

        self.hor_line = Line2D(center, slope=self.base_line.slope)
        self.left_line = Line2D(center, slope=self.left_line.slope)
        self.right_line = Line2D(center, slope=self.right_line.slope)

        self.top_points = None
        self.left_points = None
        self.right_points = None

        self.top_collision: Collision = None
        self.right_collision: Collision = None
        self.left_collision: Collision = None


    def get_triangle_vertices(self, scale: float = 1) -> list[Point]:
        opposite = scale / 2
        height = opposite / tan(radians(self.THETA / 2))

        # Points are returned (Top Point, Left Point, Right Point) of triangle
        return [Point(self.center.x(), self.center.y() + self.MEW * height, self.center.z()),
                Point(self.center.x() - opposite, self.center.y() - height + self.MEW * height, self.center.z()),
                Point(self.center.x() + opposite, self.center.y() - height + self.MEW * height, self.center.z())]


    def get_scaled_top_point(self, scale: float) -> Point:
        opposite = scale / 2
        height = opposite / tan(radians(self.THETA / 2))

        return Point(self.center.x(), self.center.y() + self.MEW * height, self.center.z())

    def get_scaled_left_point(self, scale: float) -> Point:
        opposite = scale / 2
        height = opposite / tan(radians(self.THETA / 2))

        return Point(self.center.x() - opposite, self.center.y() - height + self.MEW * height, self.center.z())

    def get_scaled_right_point(self, scale: float) -> Point:
        opposite = scale / 2
        height = opposite / tan(radians(self.THETA / 2))

        return Point(self.center.x() + opposite, self.center.y() - height + self.MEW * height, self.center.z())

    def categorize_points(self, points):
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

    def calc_scale(self, point: Point, top: bool) -> float:
        if top:
            return (point.y() - self.center.y()) / Triangle.base_height
        dist = self.center.euclidean_distance(point)
        alpha = degrees(atan(abs(point.y() - self.center.y()) / abs(point.x() - self.center.x())))
        return dist * sin(radians(180 - alpha - Triangle.DELTA)) / sin(radians(Triangle.DELTA))


    def store_top_collision(self):
        if not self.top_points:
            # ToDo: handle no collisions
            self.top_collision = Collision(point=None, scale=float('inf'), triangle=self, has_happened=True)
        else:
            scale = float('inf')
            for p in self.top_points:
                cur_scale = self.calc_scale(p, False)
                if cur_scale < scale:
                    scale = cur_scale
            self.top_collision = TopCollision(point=self.get_scaled_top_point(scale), scale=scale, triangle=self)

    def store_left_collision(self):
        if not self.left_points:
            # ToDo: handle no collisions
            self.left_collision = Collision(point=None, scale=float('inf'), triangle=self, has_happened=True)
        else:
            self.left_collision = Collision(point=None, scale=float('inf'), triangle=self)
            scale = float('inf')
            for p in self.left_points:
                cur_scale = self.calc_scale(p, False)
                if cur_scale < scale:
                    scale = cur_scale

            self.left_collision = LeftCollision(point=self.get_scaled_left_point(scale), scale=scale, triangle=self)

    def store_right_collision(self):
        if not self.right_points:
            # ToDo: handle no collisions
            self.right_collision = Collision(point=None, scale=float('inf'), triangle=self, has_happened=True)
        else:
            self.right_collision = Collision(point=None, scale=float('inf'), triangle=self)
            scale = float('inf')
            for p in self.right_points:
                cur_scale = self.calc_scale(p, False)
                if cur_scale < self.right_collision.scale:
                    scale = cur_scale

            self.right_collision = RightCollision(point=self.get_scaled_right_point(scale), scale=cur_scale,
                                                  triangle=self)

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
    def __init__(self, points):
        self.triangles = np.empty(len(points), dtype=Triangle)
        for i, p in zip(range(len(points)), points):
            self.triangles[i] = Triangle(p)
            self.triangles[i].categorize_points(points)
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
