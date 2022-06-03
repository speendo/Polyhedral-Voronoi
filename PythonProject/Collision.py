from Point import Point
from Line2D import Line2D

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
    def __init__(self, point: Point, scale: float, triangle: 'Triangle', max_x: float = 50, min_x: float = 0,
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
    def __init__(self, point: Point, scale: float, triangle: 'Triangle', max_y: float = 50, min_x: float = 0,
                 min_y: float = 0, has_happened: bool = False):
        super().__init__(point, scale, triangle, has_happened)
        self.line1 = self.generate_vertical_line(max_y)
        self.line2 = self.generate_left_line(min_x, min_y)

    def generate_vertical_line(self, max_y):
        return Line2D(point=self.point, end_point=Point(self.point.x(), max_y, 0))

    def generate_left_line(self, min_x, min_y):
        line = Line2D(point=self.point, slope=self.triangle.left_line.slope / 2)
        line.end_point = max([line.point_at_x(min_y), line.point_at_y(min_x)], key=lambda p: p.y())
        return line


class RightCollision(Collision):
    def __init__(self, point: Point, scale: float, triangle: 'Triangle', max_x: float = 50, max_y: float = 50, min_y: float = 0,
                 has_happened: bool = False):
        super().__init__(point, scale, triangle, has_happened)
        self.line1 = self.generate_vertical_line(max_y)
        self.line2 = self.generate_right_line(max_x, min_y)

    def generate_vertical_line(self, max_y):
        return Line2D(point=self.point, end_point=Point(self.point.x(), max_y, 0))

    def generate_right_line(self, max_x, min_y):
        line = Line2D(point=self.point, slope=self.triangle.right_line.slope / 2)
        line.end_point = max([line.point_at_x(min_y), line.point_at_y(max_x)], key=lambda p: p.y())
        return line