from enum import IntEnum, auto
from Point import Point


class Pos(IntEnum):
    BELOW = -1
    ABOVE = 1
    ON = 0


class Line2D:
    def __init__(self, point: Point, end_point: Point = None, slope: float = None):
        self.point: Point = point
        self.end_point: Point = end_point
        if self.end_point is not None:
            if self.end_point.x() - self.point.x() != 0:
                self.slope: float = (self.end_point.y() - self.point.y()) / (self.end_point.x() - self.point.x())
            else:
                self.slope: float = float('inf')
        else:
            self.slope: float = slope
        self.intercept = self.point.y() - self.point.x()*self.slope

    # returns +1 for above line, -1 for below line, 0 for on line
    def point_position(self, point: Point) -> Pos:
        y_value = point.x() * self.slope + self.intercept
        if point.y() > y_value:
            return Pos.ABOVE
        elif point.y() < y_value:
            return Pos.BELOW
        else:
            return Pos.ON

    def point_at_x(self, x: float) -> Point:
        return Point(x=x, y=x * self.slope + self.intercept, z=0)

    def point_at_y(self, y: float) -> Point:
        return Point(x=(y - self.intercept) / self.slope, y=y, z=0)

    def end_point_at_x(self, x: float):
        self.end_point = self.point_at_x(x)

    def end_point_at_y(self, y: float):
        self.end_point = self.point_at_y(y)

    def cross_lines(self, other_line: 'Line2D'):
        if self.slope != other_line.slope:
            x: float = 0
            if self.slope == float('inf'):
                x = self.point.x()
            elif other_line.slope == float('inf'):
                x = other_line.point.x()
            else:
                x = (other_line.intercept - self.intercept) / (self.slope - other_line.slope)

            other_line.end_point_at_x(x)
            self.end_point_at_x(x)
