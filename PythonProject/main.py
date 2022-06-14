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
    NO_POINTS = n
    THETA = t
    MEW = m
    MIN_X = 0
    MIN_Y = 0
    MIN_Z = 0
    MAX_X = 50
    MAX_Y = 50
    MAX_Z = 0

    points = [Point(glm.vec3(random.random() * MAX_X, random.random() * MAX_Y,
                             random.random() * MAX_Z), i) for i in range(NO_POINTS)]
    points = [Point(glm.vec3(13.62315845489502, 33.51239013671875, 0.0)),
              Point(glm.vec3(29.77773094177246, 3.8591370582580566, 0.0)),
              Point(glm.vec3(0.7624854445457458, 10.322636604309082, 0.0)),
              Point(glm.vec3(40.18679428100586, 43.19552993774414, 0.0)), ]

    #    Buggy inputs:
    # points = [Point(glm.vec3(28.89190101623535, 41.676185607910156, 0.0)), Point(glm.vec3(46.438045501708984, 17.486921310424805, 0.0)), Point(glm.vec3(2.3031342029571533, 10.209383964538574, 0.0)), Point(glm.vec3(34.372528076171875, 22.53403663635254, 0.0)), ]

    # points = [Point(glm.vec3(15.789161682128906, 42.6627082824707, 0.0)), Point(glm.vec3(19.750951766967773, 0.6110978126525879, 0.0)), Point(glm.vec3(45.5194091796875, 30.237092971801758, 0.0)), Point(glm.vec3(39.65787124633789, 15.787607192993164, 0.0)), Point(glm.vec3(26.34703826904297, 26.280113220214844, 0.0)), ]
    # points = [Point(glm.vec3(32.58632278442383, 40.09115219116211, 0.0)), Point(glm.vec3(15.976365089416504, 8.040189743041992, 0.0)), Point(glm.vec3(45.87504196166992, 41.5893669128418, 0.0)), Point(glm.vec3(25.068574905395508, 17.420928955078125, 0.0)), Point(glm.vec3(38.39833068847656, 39.33024597167969, 0.0)), ]

    print_points(points)

    cones = [Cone(point, THETA, MEW) for point in points]

    all_collisions = []
    for i in range(NO_POINTS):
        for j in range(i + 1, NO_POINTS):
            all_collisions.append(Collision(cones[i], cones[j]))

    all_collisions.sort(key=lambda d: d.scale)

    triangles = []
    col_points = []
    col_lines = []
    col_line_id = 1
    for collision in all_collisions:
        ignore = False
        for cone in cones:
            # If the collision happens inside a cone, it won't be valid so we ignore it
            if cone.center != collision.topCone.center and cone.center != collision.bottomCone.center \
                    and cone.point_inside_cone(collision.collision_point, collision.scale):
                ignore = True
                break
        if not ignore:
            col_points.append(collision.collision_point)
            collision.calculate_directions()
            col_lines.append(CollisionLine(Line(collision.collision_point, collision.collision_direction_1), col_line_id))
            col_line_id+=1
            col_lines.append(CollisionLine(Line(collision.collision_point, collision.collision_direction_2), col_line_id))
            col_line_id+=1

            # Create triangles for debugging
            triangles.append(collision.topCone.get_triangle_vertices(collision.scale, collision.vector_between))
            triangles.append(collision.bottomCone.get_triangle_vertices(collision.scale, collision.vector_between))

    final_lines = []
    quadBoundaryLines = [
        CollisionLine(Line(Point(glm.vec3(MIN_X, MIN_Y, MIN_Z)), glm.vec3(1, 0, 0)), col_line_id),
        CollisionLine(Line(Point(glm.vec3(MIN_X, MIN_Y, MIN_Z)), glm.vec3(0, 1, 0)), col_line_id+1),
        CollisionLine(Line(Point(glm.vec3(MAX_X, MIN_Y, MIN_Z)), glm.vec3(0, 1, 0)), col_line_id+2),
        CollisionLine(Line(Point(glm.vec3(MIN_X, MAX_Y, MIN_Z)), glm.vec3(1, 0, 0)), col_line_id+3),

        CollisionLine(Line(Point(glm.vec3(MAX_X, MIN_Y, MIN_Z)), glm.vec3(-1, 0, 0)), col_line_id+4),
        CollisionLine(Line(Point(glm.vec3(MIN_X, MAX_Y, MIN_Z)), glm.vec3(0, -1, 0)), col_line_id + 5),
        CollisionLine(Line(Point(glm.vec3(MAX_X, MAX_Y, MIN_Z)), glm.vec3(0, -1, 0)), col_line_id + 6),
        CollisionLine(Line(Point(glm.vec3(MAX_X, MAX_Y, MIN_Z)), glm.vec3(-1, 0, 0)), col_line_id + 7),

    ]

    def setCollisionLineEnd(id: int, intersectionPoint: Point):
        for col_linee in col_lines:
            if col_linee.id == id:
                col_linee.setEnd(intersectionPoint)
                final_lines.append(col_linee)
                return

    def findNextIntersection(inputLine, closestLine=None):
        if closestLine is None:
            closestLine = inputLine.findClosestIntersections(col_lines)[0]

        if not closestLine:
            # Inputline has no hit lines, i.e. it goes out of bounds
            wallHit = inputLine.findClosestIntersections(quadBoundaryLines)
            intersectionPoint = inputLine.line.findIntersection2D(wallHit[0].line)
            setCollisionLineEnd(inputLine.id, intersectionPoint)
            return False

        # We need to find out if the input line is also closest from the hit line's origin
        closestLineClosestLines = closestLine.findClosestIntersections(col_lines)

        if closestLineClosestLines[0].id == inputLine.id or closestLineClosestLines[1].id == inputLine.id:
            # We found 3 lines that form an intersection in the diagram
            intersectionPoint = inputLine.line.findIntersection2D(closestLine.line)
            setCollisionLineEnd(closestLine.id, intersectionPoint)
            setCollisionLineEnd(closestLineClosestLines[0].id, intersectionPoint)
            setCollisionLineEnd(closestLineClosestLines[1].id, intersectionPoint)
            return False

        else:
            # The hit line has a closer neighbor, we start the function again with those two lines as input
            return[closestLine, closestLineClosestLines[0]]

    i = 0
    while i < len(col_lines):
        line = col_lines[i]
        if not line.foundEnd:
            newInputLines = findNextIntersection(line)
            while newInputLines:
                print(str(i) + "/" + str(len(col_lines)))
                print(newInputLines[0], newInputLines[1])
                newInputLines = findNextIntersection(newInputLines[0], newInputLines[1])
        else:
            i += 1

        # Ideas for Cone:
        # Remove all further collisions inside the area those 3 lines form
        # (maybe research point inside non-convex hull polynomials)


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
    data = [go.Scatter3d(x=scatter_triangles[i][0], y=scatter_triangles[i][1], z=scatter_triangles[i][2], mode='lines',
                        line={'color': "lightblue"}) for i in range(len(scatter_triangles))]
    data.append(go.Scatter3d(x=scatter_points[0], y=scatter_points[1], z=scatter_points[2],
                             mode='markers', marker={'color': 'blue'}))
    for scatter_line in scatter_lines:
        data.append(go.Scatter3d(x=scatter_line[0], y=scatter_line[1], z=scatter_line[2], mode='lines', line={'color': 'black'}))
    # Collisions: data.append(go.Scatter3d(x=scatter_collisions[0], y=scatter_collisions[1], z=scatter_collisions[2],
    #                                      mode='markers', marker={'color': 'red'}))


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
