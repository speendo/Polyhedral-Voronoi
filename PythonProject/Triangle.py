from math import tan, radians, degrees, atan, sin
from typing import final

import numpy as np

from Line2D import Line2D
from Point import Point, Points


class Collision:
    def __init__(self, point: Point, scale: float, has_happened: bool = False):
        self.point = point
        self.scale = scale
        self.has_happened = has_happened

    def collide(self):
        self.has_happened = True


def get_triangle_vertices(p: Point, mew: float, height: float, scale: float = 1) -> list[Point]:
    opposite = scale / 2

    # Points are returned (Top Point, Left Point, Right Point) of triangle
    return [Point(p.x(), p.y() + mew * height, p.z()),
            Point(p.x() - opposite, p.y() - height + mew * height, p.z()),
            Point(p.x() + opposite, p.y() - height + mew * height, p.z())]


class Triangle:
    THETA: final = 30
    MEW: final = 0.5
    DELTA: final = (180 - THETA) / 2

    base_height = 1 / 2 / tan(radians(THETA / 2))

    origin_triangle = get_triangle_vertices(p=Point(0, 0, 0), mew=MEW, height=base_height)
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
        return get_triangle_vertices(p=self.center, mew=self.MEW, height=self.base_height, scale=scale)

    def categorize_points(self, points: Points):
        self.top_points = []
        self.left_points = []
        self.right_points = []

        for p in points:
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
<<<<<<< HEAD
        if not self.top_points:
            # ToDo: handle no collisions
            self.top_collision = Collision(point=None, scale=float('inf'), has_happened=True)
        else:
            top_collision_point = min(self.top_points, key=lambda p: p.y())
            top_scale_to_hit = self.calc_top_scale(self.top_collision_point)
            self.top_collision = Collision(top_collision_point, top_scale_to_hit)

    def store_left_collision(self):
        if not self.left_points:
            # ToDo: handle no collisions
            self.left_collision = Collision(point=None, scale=float('inf'), has_happened=True)
        else:
            self.left_collision = Collision(None, float('inf'))
            for p in self.left_points:
                cur_scale = self.calc_side_scale(p)
                if cur_scale < self.left_collision.scale:
                    self.left_collision = Collision(p, cur_scale)

    def store_right_collision(self):
        if not self.right_points:
            # ToDo: handle no collisions
            self.top_collision = Collision(point=None, scale=float('inf'), has_happened=True)
        else:
            self.right_collision = Collision(None, float('inf'))
            for p in self.right_points:
                cur_scale = self.calc_side_scale(p)
                if cur_scale < self.right_collision.scale:
                    self.right_collision = Collision(p, cur_scale)

    def store_collisions(self):
        self.store_top_collision()
        self.store_left_collision()
        self.store_right_collision()

    def find_next_collision(self) -> Collision:
        return min([self.top_collision, self.left_collision, self.right_collision],
                   key=lambda c: float('Inf') if c is None or c.has_happened else c.scale)


class Triangles:
    def __init__(self, points: Points):
        self.triangles = np.empty(points.get().size, dtype=Triangle)
        for i, p in zip(range(points.get().size), points.get()):
            self.triangles[i] = Triangle(p)
            self.triangles[i].categorize_points(points.get())
            self.triangles[i].store_collisions()

    def get(self):
        return self.triangles

    def find_next_collision(self) -> Collision:
        return min(self.triangles, key=lambda t: t.find_next_collision().scale)
=======
        top_collision_point = min(self.top_points, key=lambda p: p.y())
        top_scale_to_hit = self.calc_top_scale(self.top_collision_point)
        self.top_collision = Collision(top_collision_point, top_scale_to_hit)

    def store_left_collision(self):
        self.left_collision = Collision(None, float('inf'))
        for p in self.left_points:
            cur_scale = self.calc_side_scale(p)
            if cur_scale < self.left_collision.scale:
                self.left_collision = Collision(p, cur_scale)

    def store_right_collision(self):
        self.right_collision = Collision(None, float('inf'))
        for p in self.right_points:
            cur_scale = self.calc_side_scale(p)
            if cur_scale < self.right_collision.scale:
                self.right_collision = Collision(p, cur_scale)

    def find_next_collision(self) -> Collision:
        return min([self.top_collision, self.left_collision, self.right_collision],
                   key=lambda c: float('inf') if c.has_happened else c.scale)
>>>>>>> origin/Marcel's_Refactor
