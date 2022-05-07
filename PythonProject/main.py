from math import sin, tan, atan, radians, degrees
from typing import final
import random

import plotly.graph_objects as go
import numpy as np

from Point import Point

NO_POINTS: final = 2


def points_to_scatter(point_array, form_triangle: bool):
    x_array = [point.x() for point in point_array]
    y_array = [point.y() for point in point_array]
    z_array = [point.z() for point in point_array]
    if form_triangle:
        x_array.append(point_array[0].x())
        y_array.append(point_array[0].y())
        z_array.append(point_array[0].z())
    return [x_array, y_array, z_array]


def calculate_meeting_scale(p1: Point, p2: Point):
    # TODO: if im oberen sektor is anders berechnen
    #       return y difference / height
    dist = p1.euclidean_distance(p2)
    alpha = degrees(atan(abs(p1.y() - p2.y()) / abs(p1.x() - p2.x())))
    return dist * sin(radians(180 - alpha - DELTA)) / sin(radians(DELTA))


def main():
    scale = 1

    points = [Point(np.random.uniform(0, 10), np.random.uniform(0, 10), 0.5) for _ in range(NO_POINTS)]
    triangles = [get_triangle_vertices(points[i], scale) for i in range(NO_POINTS)]

    scatter_triangles = []
    for triangle in triangles:
        scatter_triangles.append(points_to_scatter(triangle, True))

    # TODO: insert loop und alles andere
    new_scale = calculate_meeting_scale(points[0], points[1])

    triangles = [get_triangle_vertices(points[i], new_scale) for i in range(NO_POINTS)]
    for triangle in triangles:
        scatter_triangles.append(points_to_scatter(triangle, True))

    scatter_points = points_to_scatter(points, False)

    colors = ["#%06x" % random.randint(0, 0xFFFFFF) for _ in range(NO_POINTS)]
    data = [go.Scatter3d(x=scatter_triangles[i][0], y=scatter_triangles[i][1], z=scatter_triangles[i][2],
                         mode='lines', line={'color': colors[i % NO_POINTS]}) for i in range(len(scatter_triangles))]
    data.append(go.Scatter3d(x=scatter_points[0], y=scatter_points[1], z=scatter_points[2], mode='markers'))

    fig = go.Figure(data=data)
    fig.update_layout(
        scene=dict(
            xaxis=dict(tickmode="linear", range=[-5, 15], linewidth=1),
            yaxis=dict(tickmode="linear", range=[-5, 15], linewidth=1),
            zaxis=dict(tickmode="linear", range=[-5, 15], linewidth=1),
        ))
    fig.show()


if __name__ == '__main__':
    main()
