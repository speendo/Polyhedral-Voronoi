import sys
from math import sin, tan, atan, radians, degrees
from typing import final
import random

import plotly.graph_objects as go
import numpy as np
import glm  # install PyGLM

from Point import Point
from Cone import Cone, Distance
from Triangle import Triangles


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

    distances = []
    for i in range(NO_POINTS):
        for j in range(i+1, NO_POINTS):
            distances.append(Distance(cones[i], cones[j]))

    distances.sort(key=lambda d: d.scale)

    triangles = []
    for distance in distances:
        vector_between = distance.c1.CENTER.vectorBetween(distance.c2.CENTER)
        triangles.append(distance.c1.get_triangle_vertices(distance.scale, vector_between))
        triangles.append(distance.c2.get_triangle_vertices(distance.scale, vector_between))
        break

    scatter_points = points_to_scatter(points, False)
    scatter_triangles = []
    for triangle in triangles:
        scatter_triangles.append(points_to_scatter(triangle, True))

    colors = ["#%06x" % random.randint(0, 0xFFFFFF) for _ in range(NO_POINTS)]
    data = [go.Scatter3d(x=scatter_triangles[i][0], y=scatter_triangles[i][1], z=scatter_triangles[i][2],
                         mode='lines', line={'color': colors[i % NO_POINTS]}) for i in range(len(scatter_triangles))]
    data.append(go.Scatter3d(x=scatter_points[0], y=scatter_points[1], z=scatter_points[2],
                             mode='markers', marker={'color': 'blue'}))

    # data.append(go.Scatter3d(x=scatter_collisions[0], y=scatter_collisions[1], z=scatter_collisions[2],
    #                         mode='markers', marker={'color': 'red'}))

    fig = go.Figure(data=data)
    fig.update_layout(
        scene=dict(
            xaxis=dict(tickmode="linear", range=[-30, MAX_X+30], linewidth=1),
            yaxis=dict(tickmode="linear", range=[-30, MAX_Y+30], linewidth=1),
            zaxis=dict(tickmode="linear", range=[-30, MAX_Z+30], linewidth=1),
        ))
    fig.show()


if __name__ == '__main__':
    if len(sys.argv) > 3 and 0 <= float(sys.argv[3]) <= 1 and 0 <= float(sys.argv[2]) <= 90:
        main(int(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3]))
    else:
        print("Usage: main.py <Number of points (ℕ)> <Theta (degrees, 0.0-90.0)> <Mew (scalar, 0.0-1.0)>")

