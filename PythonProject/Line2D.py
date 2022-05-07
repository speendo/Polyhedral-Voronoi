from Point import Point


class Line2D:
    def __init__(self, point: Point, end_point: Point = None, slope: float = None):
        self.point: Point = point
        self.end_point: Point = end_point
        if self.end_point is not None:
            self.slope: float = (self.end_point.y() - self.point.y()) / (self.end_point.x() - self.point.x())
        else:
            self.slope: float = slope
        self.intercept = self.point.y() - self.point.x()*self.slope

    # returns +1 for above line, -1 for below line, 0 for on line
    def point_position(self, point: Point) -> int:
        y_value = point.x() * self.slope + self.intercept
        if point.y() > y_value:
            return +1
        elif point.y() < y_value:
            return -1
        else:
            return 0
