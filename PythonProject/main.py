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
    MAX_X = 50
    MAX_Y = 50
    MAX_Z = 0

    points = [Point(glm.vec3(random.random() * MAX_X, random.random() * MAX_Y,
                             random.random() * MAX_Z), i) for i in range(NO_POINTS)]

    print_points(points)

    cones = [Cone(point, THETA, MEW) for point in points]

    possible_collisions = []
    for i in range(NO_POINTS):
        for j in range(i + 1, NO_POINTS):
            possible_collisions.append(Collision(cones[i], cones[j]))

    possible_collisions.sort(key=lambda d: d.scale)

    triangles = []
    col_points = []
    lines = []
    col_lines = []
    for collision in possible_collisions:
        ignore = False
        for cone in cones:
            if cone.center != collision.topCone.center and cone.center != collision.bottomCone.center \
                    and cone.point_inside_cone(collision.collision_point, collision.scale):
                ignore = True
                break
        if not ignore:
            triangles.append(collision.topCone.get_triangle_vertices(collision.scale, collision.vector_between))
            triangles.append(collision.bottomCone.get_triangle_vertices(collision.scale, collision.vector_between))

            col_points.append(collision.collision_point)

            collision.calculate_directions()
            col_lines.append(CollisionLine(Line(collision.collision_point, collision.collision_direction_1)))
            col_lines.append(CollisionLine(Line(collision.collision_point, collision.collision_direction_2)))

    for line in col_lines:
        print()
        # Find first Hit of Line
        # Try hitted line for an earlier hit (repeat)
        # If it is first, two lines should be equidistant, create collision_line_collision

        # Ideas for Cone:
        # Remove all further collisions inside the area those 3 lines form
        # (maybe research point inside non-convex hull polynomials)

    for line in col_lines:
        lines.append([line.line.p.coords, line.line.p.coords + line.line.norm_dir * 100])

    scatter_points = points_to_scatter(points, False)
    scatter_triangles = []
    for triangle in triangles:
        scatter_triangles.append(points_to_scatter(triangle, True))
    scatter_lines = []
    for line in lines:
        scatter_lines.append(points_to_scatter(line, False))
    scatter_collisions = points_to_scatter(col_points, False)

    data = [go.Scatter3d(x=scatter_triangles[i][0], y=scatter_triangles[i][1], z=scatter_triangles[i][2],
                         mode='lines', line={'color': "#%06x" % random.randint(0, 0xFFFFFF)}) for i in range(len(scatter_triangles))]
    data.append(go.Scatter3d(x=scatter_points[0], y=scatter_points[1], z=scatter_points[2],
                             mode='markers', marker={'color': 'blue'}))
    """
    data.append(go.Scatter3d(x=scatter_collisions[0], y=scatter_collisions[1], z=scatter_collisions[2],
                             mode='markers', marker={'color': 'red'}))
    """
    for scatter_line in scatter_lines:
        data.append(go.Scatter3d(x=scatter_line[0], y=scatter_line[1], z=scatter_line[2],
                                 mode='lines', line={'color': 'black'}))

    fig = go.Figure(data=data)
    fig.update_layout(
        scene=dict(
            xaxis=dict(tickmode="linear", range=[0, MAX_X], linewidth=1),
            yaxis=dict(tickmode="linear", range=[0, MAX_Y], linewidth=1),
            zaxis=dict(tickmode="linear", range=[0, MAX_Z], linewidth=1),
        ))
    fig.show()


if __name__ == '__main__':
    if len(sys.argv) > 3 and 0 <= float(sys.argv[3]) <= 1 and 0 <= float(sys.argv[2]) <= 90:
        main(int(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3]))
    else:
        print("Usage: main.py <Number of points (ℕ)> <Theta (degrees, 0.0-90.0)> <Mew (scalar, 0.0-1.0)>")
