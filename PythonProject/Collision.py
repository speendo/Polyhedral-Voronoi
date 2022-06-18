from math import degrees, atan
import glm

from Point import Point
from Line import Line
from Cone import Cone

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
        topConeTriangle = self.topCone.get_triangle_vertices(self.scale + 10, self.vector_between)
        bottomConeTriangle = self.bottomCone.get_triangle_vertices(self.scale + 10, self.vector_between)

        topConeBase = Line(topConeTriangle[1], end=topConeTriangle[2])

        if self.topCollision:  # In 3D an expanding cone from collision in direction (0, -1, 0)
            bottomConeLeft = Line(bottomConeTriangle[0], end=bottomConeTriangle[1])
            bottomConeRight = Line(bottomConeTriangle[0], end=bottomConeTriangle[2])
            intersection_1 = topConeBase.findIntersection2D(bottomConeLeft)
            intersection_2 = topConeBase.findIntersection2D(bottomConeRight)
            self.collision_direction_1 = glm.vec3(0.755929, -0.654654, 0)
            self.collision_direction_2 = glm.vec3(-0.755929, -0.654654, 0)

        else:  # In 3D an elliptical-sphere like surface, maybe a sideways cone
            if self.topCone.center.x > self.bottomCone.center.x:
                bottomConeRight = Line(bottomConeTriangle[0], end=bottomConeTriangle[2])
                topConeLeft = Line(topConeTriangle[0], end=topConeTriangle[1])
                intersection_1 = bottomConeRight.findIntersection2D(topConeLeft)
                intersection_2 = bottomConeRight.findIntersection2D(topConeBase)
                self.collision_direction_1 = glm.vec3(0,1,0)
                self.collision_direction_2 = glm.vec3(0.755929, -0.654654, 0)
            else:
                bottomConeLeft = Line(bottomConeTriangle[0], end=bottomConeTriangle[1])
                topConeRight = Line(topConeTriangle[0], end=topConeTriangle[2])
                intersection_1 = bottomConeLeft.findIntersection2D(topConeRight)
                intersection_2 = bottomConeLeft.findIntersection2D(topConeBase)
                self.collision_direction_1 = glm.vec3(-0.755929, -0.654654, 0)
                self.collision_direction_2 = glm.vec3(0,1,0)

        #self.collision_direction_1 = glm.normalize(self.collision_point.vectorFromTo(intersection_1))
        #self.collision_direction_2 = glm.normalize(self.collision_point.vectorFromTo(intersection_2))
        print(self.collision_direction_1)
        print(self.collision_direction_2)



class CollisionLine:
    foundEnd: bool = False
    line: Line
    id: int

    def __init__(self, line: Line, id: int):
        self.line = line
        self.id = id

    def findClosestIntersections(self, col_lines):
        # return closest 2 intersections
        from Line import Line
        closestLine1 = CollisionLine(Line(Point(glm.vec3(0,0,0)), glm.vec3(0,0,1)), 0)
        closestLine2 = CollisionLine(Line(Point(glm.vec3(0,0,0)), glm.vec3(0,0,1)), 0)
        closestDistance1 = float('inf')
        closestDistance2 = float('inf')

        for other_col_line in col_lines:
            if not other_col_line.foundEnd:
                if other_col_line.line.p.coords != self.line.p.coords:
                    intersectionPoint = self.line.findIntersection2D(other_col_line.line)
                    if intersectionPoint:
                        # check if point actually on line direction and not behind
                        if glm.dot(glm.normalize(self.line.p.vectorFromTo(intersectionPoint)), self.line.norm_dir) > 0:
                            if glm.dot(glm.normalize(other_col_line.line.p.vectorFromTo(intersectionPoint)), other_col_line.line.norm_dir) > 0:
                                intersectionDistance = self.line.p.euclidean_distance(intersectionPoint)
                                if intersectionDistance < closestDistance1:
                                    closestLine2 = CollisionLine(Line(closestLine1.line.p, closestLine1.line.norm_dir), closestLine1.id)
                                    closestDistance2 = closestDistance1
                                    closestLine1 = CollisionLine(Line(other_col_line.line.p, other_col_line.line.norm_dir), other_col_line.id)
                                    closestDistance1 = intersectionDistance
                                elif intersectionDistance < closestDistance2:
                                    closestLine2 = CollisionLine(Line(other_col_line.line.p, other_col_line.line.norm_dir), other_col_line.id)
                                    closestDistance2 = intersectionDistance

        if closestDistance1 == float('inf'):
            return [False, False]
        if closestDistance2 == float('inf'):
            return [closestLine1, False]
        return [closestLine1, closestLine2]

    def setEnd(self, p: Point):
        self.line.end = p
        self.foundEnd = True
