import sys
import random
from typing import final

import glm  # pip install PyGLM
import plotly.graph_objects as go

from Cone import Cone, Collision
from Point import Point


def points_to_scatter(point_array, form_triangle: bool):
    x_array = [point.x for point in point_array]
    y_array = [point.y for point in point_array]
    z_array = [point.z for point in point_array]
    if form_triangle:
        x_array.append(point_array[0].x)
        y_array.append(point_array[0].y)
        z_array.append(point_array[0].z)
    return [x_array, y_array, z_array]


def main(n, t, m):
    NO_POINTS: final = n
    THETA: final = t
    MEW: final = m
    MAX_X: final = 50
    MAX_Y: final = 50
    MAX_Z: final = 0

    points = [Point(glm.vec3(random.random() * MAX_X, random.random() * MAX_Y,
                             random.random() * MAX_Z), i) for i in range(NO_POINTS)]

    cones = [Cone(point, THETA, MEW) for point in points]

    possible_collisions = []
    for i in range(NO_POINTS):
        for j in range(i + 1, NO_POINTS):
            possible_collisions.append(Collision(cones[i], cones[j]))

    possible_collisions.sort(key=lambda d: d.scale)

    triangles = []
    col_points = []
    for collision in possible_collisions:
        triangles.append(collision.c1.get_triangle_vertices(collision.scale, collision.vector_between))
        triangles.append(collision.c2.get_triangle_vertices(collision.scale, collision.vector_between))
        col_points.append(collision.collision_point)
        # Create Lines from Point
        # Scale lines with scaling as well, figure out when 3 lines collide
        # Remove all further collisions inside the area those 3 lines form
        # (maybe research point inside non-convex hull polynomials)

    scatter_points = points_to_scatter(points, False)
    scatter_triangles = []
    for triangle in triangles:
        scatter_triangles.append(points_to_scatter(triangle, True))
    scatter_collisions = points_to_scatter(col_points, False)

    colors = ["#%06x" % random.randint(0, 0xFFFFFF) for _ in range(NO_POINTS)]
    data = [go.Scatter3d(x=scatter_triangles[i][0], y=scatter_triangles[i][1], z=scatter_triangles[i][2],
                         mode='lines', line={'color': colors[i % NO_POINTS]}) for i in range(len(scatter_triangles))]
    data.append(go.Scatter3d(x=scatter_points[0], y=scatter_points[1], z=scatter_points[2],
                             mode='markers', marker={'color': 'blue'}))
    data.append(go.Scatter3d(x=scatter_collisions[0], y=scatter_collisions[1], z=scatter_collisions[2],
                             mode='markers', marker={'color': 'red'}))

    fig = go.Figure(data=data)
    fig.update_layout(
        scene=dict(
            xaxis=dict(tickmode="linear", range=[-30, MAX_X + 30], linewidth=1),
            yaxis=dict(tickmode="linear", range=[-30, MAX_Y + 30], linewidth=1),
            zaxis=dict(tickmode="linear", range=[-30, MAX_Z + 30], linewidth=1),
        ))
    fig.show()

    print("points = [", end='')
    for point in points:
        print("Point(glm.vec3("+str(point.x)+", "+str(point.y)+", "+str(point.z)+")), ", end='')
    print("]")


if __name__ == '__main__':
    if len(sys.argv) > 3 and 0 <= float(sys.argv[3]) <= 1 and 0 <= float(sys.argv[2]) <= 90:
        main(int(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3]))
    else:
        print("Usage: main.py <Number of points (ℕ)> <Theta (degrees, 0.0-90.0)> <Mew (scalar, 0.0-1.0)>")
