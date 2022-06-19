import sys
import random

import glm  # pip install PyGLM
import plotly.graph_objects as go

from Point import Point
from Line import Line
from Cone import Cone
from Collision import Collision, CollisionLine


def points_to_scatter(point_array, form_triangle: bool):
    x_array = [point.x for point in point_array]
    y_array = [point.y for point in point_array]
    z_array = [point.z for point in point_array]
    if form_triangle:
        x_array.append(point_array[0].x)
        y_array.append(point_array[0].y)
        z_array.append(point_array[0].z)
    return [x_array, y_array, z_array]


def print_points(points):
    print("Want to recreate the same inputs? Copy line below:")
    print("points = [", end='')
    for point in points:
        print("Point(glm.vec3(" + str(point.x) + ", " + str(point.y) + ", " + str(point.z) + ")), ", end='')
    print("]")



def main(n, t, m):
    drawAllCollisions = False
    NO_POINTS = n
    THETA = t
    MEW = m
    MIN_X = 0
    MIN_Y = 0
    MIN_Z = 0
    MAX_X = 1000
    MAX_Y = 1000
    MAX_Z = 0

    points = [Point(glm.vec3(random.random() * MAX_X, random.random() * MAX_Y,
                             random.random() * MAX_Z), i) for i in range(NO_POINTS)]
    #   Buggy inputs:
    # (None)
    print_points(points)

    cones = [Cone(points[i], THETA, MEW, i) for i in range(len(points))]

    all_collisions = []
    for i in range(NO_POINTS):
        for j in range(i + 1, NO_POINTS):
            all_collisions.append(Collision(cones[i], cones[j]))

    all_collisions.sort(key=lambda d: d.scale)

    triangles = []
    col_points = []
    col_lines = []
    col_line_id = 0
    final_lines = []

    def setCollisionLineEnd(id: int, intersectionPoint: Point):
        for col_linee in col_lines:
            if col_linee.id == id:
                print("End of the line: " + str(id))
                col_linee.setEnd(intersectionPoint)
                final_lines.append(col_linee)
                return


    for collision in all_collisions:
        ignore = False
        for cone in cones:
            # If the collision happens inside a cone, it won't be valid so we ignore it
            if cone.center != collision.topCone.center and cone.center != collision.bottomCone.center \
                    and cone.point_inside_cone(collision.collision_point, collision.scale):
                ignore = True
                break
        if not ignore:
            # Add collision
            col_points.append(collision.collision_point)
            collision.calculate_directions()
            col_lines.append(CollisionLine(Line(collision.collision_point, collision.collision_direction_1),
                                           collision.coneIDs, col_line_id))
            col_line_id += 1
            col_lines.append(CollisionLine(Line(collision.collision_point, collision.collision_direction_2),
                                           collision.coneIDs, col_line_id))
            col_line_id += 1

            # Create triangles for debugging
            triangles.append(collision.topCone.get_triangle_vertices(collision.scale, collision.vector_between))
            triangles.append(collision.bottomCone.get_triangle_vertices(collision.scale, collision.vector_between))

            # Check if any intersection is happening
            for col_line in col_lines:
                breakFlag = False
                if not col_line.foundEnd:
                    coneIDs = col_line.coneIDs
                    for other_col_line in col_lines:
                        # check if they're not from the same collision
                        if not other_col_line.foundEnd:
                            if other_col_line.id != col_line.id:
                                # check if they share the first coneID
                                otherConeIDs = other_col_line.coneIDs
                                if coneIDs[0] == otherConeIDs[0]:
                                    # we search for a third collision which has the missing 2 IDs
                                    missingIDs = [coneIDs[1], otherConeIDs[1]]
                                    missingIDs.sort()
                                    for third_col_line in col_lines:
                                        if not third_col_line.foundEnd:
                                            if missingIDs == third_col_line.coneIDs:
                                                # there are always 2 of those, so we need to check which intersects
                                                intersections = col_line.findClosestIntersections([other_col_line, third_col_line])
                                                if intersections[1]:
                                                    # The three lines intersect (yay)
                                                    intersectionPoint = col_line.line.findIntersection2D(other_col_line.line)
                                                    # We found 3 lines that form an intersection in the diagram
                                                    setCollisionLineEnd(col_line.id, intersectionPoint)
                                                    setCollisionLineEnd(other_col_line.id, intersectionPoint)
                                                    setCollisionLineEnd(third_col_line.id, intersectionPoint)
                                                    breakFlag = True
                                                    break
                                    if breakFlag:
                                        break



    quadBoundaryLines = [
        CollisionLine(Line(Point(glm.vec3(MIN_X, MIN_Y, MIN_Z)), glm.vec3(1, 0, 0)), [0,0], col_line_id),
        CollisionLine(Line(Point(glm.vec3(MIN_X, MIN_Y, MIN_Z)), glm.vec3(0, 1, 0)), [0,0], col_line_id+1),
        CollisionLine(Line(Point(glm.vec3(MAX_X, MIN_Y, MIN_Z)), glm.vec3(0, 1, 0)), [0,0], col_line_id+2),
        CollisionLine(Line(Point(glm.vec3(MIN_X, MAX_Y, MIN_Z)), glm.vec3(1, 0, 0)), [0,0], col_line_id+3),

        CollisionLine(Line(Point(glm.vec3(MAX_X, MIN_Y, MIN_Z)), glm.vec3(-1, 0, 0)), [0,0], col_line_id+4),
        CollisionLine(Line(Point(glm.vec3(MIN_X, MAX_Y, MIN_Z)), glm.vec3(0, -1, 0)), [0,0], col_line_id + 5),
        CollisionLine(Line(Point(glm.vec3(MAX_X, MAX_Y, MIN_Z)), glm.vec3(0, -1, 0)), [0,0], col_line_id + 6),
        CollisionLine(Line(Point(glm.vec3(MAX_X, MAX_Y, MIN_Z)), glm.vec3(-1, 0, 0)), [0,0], col_line_id + 7),

    ]

    # Handle all collisions with 1 other point or wall
    for col_line in col_lines:
        if not col_line.foundEnd:
            wallHit = col_line.findClosestIntersections(quadBoundaryLines)
            intersectionPoint = col_line.line.findIntersection2D(wallHit[0].line)
            setCollisionLineEnd(col_line.id, intersectionPoint)


    """
    def findNextIntersection(inputLine, closestLines=None):
        if closestLines is None:
            closestLines = inputLine.findClosestIntersections(col_lines)

        closestLine = closestLines[0]
        secondClosestLine = closestLines[1]

        if not closestLine:
            # Inputline has no hit lines, i.e. it goes out of bounds
            wallHit = inputLine.findClosestIntersections(quadBoundaryLines)
            intersectionPoint = inputLine.line.findIntersection2D(wallHit[0].line)
            setCollisionLineEnd(inputLine.id, intersectionPoint)
            return False

        if secondClosestLine:
            intersectionPoint = inputLine.line.findIntersection2D(closestLine.line)
            intersectionPoint2 = inputLine.line.findIntersection2D(secondClosestLine.line)
            if intersectionPoint.euclidean_distance(intersectionPoint2) < 0.1:
                # We found 3 lines that form an intersection in the diagram
                setCollisionLineEnd(inputLine.id, intersectionPoint)
                setCollisionLineEnd(closestLine.id, intersectionPoint)
                setCollisionLineEnd(secondClosestLine.id, intersectionPoint)
                return False

        # The 3 lines do not form an intersectionPoint
        # We need to find out if the input line is also closest from the hit line's origin
        closestLineClosestLines = closestLine.findClosestIntersections(col_lines)

        if closestLineClosestLines[0].id == inputLine.id:
            intersectionPoint = closestLineClosestLines[0].line.findIntersection2D(closestLine.line)
            setCollisionLineEnd(closestLine.id, intersectionPoint)
            setCollisionLineEnd(closestLineClosestLines[0].id, intersectionPoint)
            if closestLineClosestLines[1]:
                intersectionPoint2 = closestLineClosestLines[1].line.findIntersection2D(closestLine.line)
                if intersectionPoint.euclidean_distance(intersectionPoint2) < 0.1:
                    setCollisionLineEnd(closestLineClosestLines[1].id, intersectionPoint)
            return False

        elif closestLineClosestLines[1] and closestLineClosestLines[1].id == inputLine.id:
            intersectionPoint = closestLineClosestLines[1].line.findIntersection2D(closestLine.line)
            setCollisionLineEnd(closestLine.id, intersectionPoint)
            setCollisionLineEnd(closestLineClosestLines[1].id, intersectionPoint)
            intersectionPoint2 = closestLineClosestLines[0].line.findIntersection2D(closestLine.line)
            if intersectionPoint.euclidean_distance(intersectionPoint2) < 0.1:
                setCollisionLineEnd(closestLineClosestLines[0].id, intersectionPoint)
            return False

        else:
            # The hit line has a closer neighbor, we start the function again with those two lines as input
            return[closestLine, closestLineClosestLines]

    i = 0
    if drawAllCollisions:
    i = len(col_lines)
    final_lines = col_lines
    while i < len(col_lines):
        print(str(i) + "/" + str(len(col_lines)))
        line = col_lines[i]
        if not line.foundEnd:
            newInputLines = findNextIntersection(line)
            while newInputLines:
                print(str(i) + "/" + str(len(col_lines)))
                print(newInputLines[0].id, newInputLines[1][0].id, newInputLines[1][1].id)
                newInputLines = findNextIntersection(newInputLines[0], newInputLines[1])
        else:
            i += 1

        # Ideas for Cone:
        # Remove all further collisions inside the area those 3 lines form
        # (maybe research point inside non-convex hull polynomials)
    """

    """Render Stuff"""

    lines = []

    for col_line in final_lines:
        line = col_line.line
        if line.end is not None:
            lines.append([line.p.coords, line.end.coords])
        else:
            lines.append([line.p.coords, line.p.coords + line.norm_dir * 100])

    scatter_points = points_to_scatter(points, False)
    scatter_triangles = []
    for triangle in triangles:
        scatter_triangles.append(points_to_scatter(triangle, True))
    scatter_lines = []
    for line in lines:
        scatter_lines.append(points_to_scatter(line, False))
    scatter_collisions = points_to_scatter(col_points, False)


    data = []
    data.append(go.Scatter3d(x=scatter_points[0], y=scatter_points[1], z=scatter_points[2],
                             mode='markers', marker={'color': 'blue'}))
    for scatter_line in scatter_lines:
        data.append(go.Scatter3d(x=scatter_line[0], y=scatter_line[1], z=scatter_line[2], mode='lines',
                                 line={'color': 'black'}))
    """
    for scatter_triangle in scatter_triangles:
        data.append(go.Scatter3d(x=scatter_triangle[0], y=scatter_triangle[1], z=scatter_triangle[2], mode='lines',
                                 line={'color': "lightblue"}))
    """
    # data.append(go.Scatter3d(x=scatter_collisions[0], y=scatter_collisions[1], z=scatter_collisions[2],
    #                                     mode='markers', marker={'color': 'red'}))


    fig = go.Figure(data=data)
    fig.update_layout(
        scene=dict(
            xaxis=dict(tickmode="linear", range=[MIN_X, MAX_X], linewidth=1),
            yaxis=dict(tickmode="linear", range=[MIN_Y, MAX_Y], linewidth=1),
            zaxis=dict(tickmode="linear", range=[MIN_Z, MAX_Z], linewidth=1),
        ))
    fig.show()


if __name__ == '__main__':
    if len(sys.argv) > 3 and 0 <= float(sys.argv[3]) <= 1 and 0 <= float(sys.argv[2]) <= 90:
        main(int(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3]))
    else:
        print("Usage: main.py <Number of points (ℕ)> <Theta (degrees, 0.0-90.0)> <Mew (scalar, 0.0-1.0)>")
