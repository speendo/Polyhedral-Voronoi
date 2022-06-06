import glm
from Point import Point
import numpy as np


class Line:
    p: Point
    norm_dir: glm.vec3
    end: Point = None

    def __init__(self, point: Point, direction: glm.vec3 = None, end: Point = None):
        self.p = point
        if direction is None:
            self.norm_dir = glm.normalize(end.vectorFromTo(point))
        else:
            self.norm_dir = glm.normalize(direction)

    def findIntersection2D(self, otherLine: 'Line'):

        def get_intersect(a1, a2, b1, b2):
            # https://stackoverflow.com/a/42727584
            """
            Returns the point of intersection of the lines passing through a2,a1 and b2,b1.
            a1: [x, y] a point on the first line
            a2: [x, y] another point on the first line
            b1: [x, y] a point on the second line
            b2: [x, y] another point on the second line
            """
            s = np.vstack([a1, a2, b1, b2])  # s for stacked
            h = np.hstack((s, np.ones((4, 1))))  # h for homogeneous
            l1 = np.cross(h[0], h[1])  # get first line
            l2 = np.cross(h[2], h[3])  # get second line
            x, y, z = np.cross(l1, l2)  # point of intersection
            if z == 0:  # lines are parallel
                return [float('inf'), float('inf')]
            return [x / z, y / z]

        p1 = [self.p.x, self.p.y]
        p2 = [self.p.x + self.norm_dir.x, self.p.y + self.norm_dir.y]
        q1 = [otherLine.p.x, otherLine.p.y]
        q2 = [otherLine.p.x + otherLine.norm_dir.x, otherLine.p.y + otherLine.norm_dir.y]
        intersection = get_intersect(p1, p2, q1, q2)
        if intersection[0] == float('inf'):
            return False
        return Point(glm.vec3(intersection[0], intersection[1], 0))
