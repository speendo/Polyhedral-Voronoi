from math import sin, tan, atan, radians, degrees
from typing import final
import random

import plotly.graph_objects as go
import numpy as np

from Point import Point, Points
from Triangle import Triangle, Triangles, Collision

NO_POINTS: final = 3
max_x = 50
max_y = 50
max_z = 0


def points_to_scatter(point_array, form_triangle: bool):
    x_array = [point.x() for point in point_array]
    y_array = [point.y() for point in point_array]
    z_array = [point.z() for point in point_array]
    if form_triangle:
        x_array.append(point_array[0].x())
        y_array.append(point_array[0].y())
        z_array.append(point_array[0].z())
    return [x_array, y_array, z_array]


def main():
    points = Points(number_of_points=NO_POINTS, max_x=max_x, max_y=max_y, max_z=max_z)
    points.set_random()

    triangles = Triangles(points)

    scatter_triangles = []
    for triangle in triangles.get():
        scatter_triangles.append(points_to_scatter(triangle.get_scaled_points(scale=1), True))

    collisions = []
    scale_list = []
    while triangles.has_next_collision():
        col = triangles.find_next_collision()
        scale_list.append(col.get_scale())
        col.collide()
        collisions.append(col)

    collisions_points = []
    for triangle in triangles.get():
        point = triangle.top_collision.point
        if point is not None:
            collisions_points.append(point)
        point = triangle.left_collision.point
        if point is not None:
            collisions_points.append(point)
        point = triangle.right_collision.point
        if point is not None:
            collisions_points.append(point)

    scatter_collisions = points_to_scatter(collisions_points, False)

    for scale in scale_list:
        for triangle in triangles.get():
            scatter_triangles.append(points_to_scatter(triangle.get_scaled_points(scale=scale), True))

    scatter_points = points_to_scatter(points.get(), False)

    colors = ["#%06x" % random.randint(0, 0xFFFFFF) for _ in range(NO_POINTS)]
    data = [go.Scatter3d(x=scatter_triangles[i][0], y=scatter_triangles[i][1], z=scatter_triangles[i][2],
                         mode='lines', line={'color': colors[i % NO_POINTS]}) for i in range(len(scatter_triangles))]
    #data.append(go.Scatter3d(x=scatter_points[0], y=scatter_points[1], z=scatter_points[2], mode='markers'))
    data.append(go.Scatter3d(x=scatter_collisions[0], y=scatter_collisions[1], z=scatter_collisions[2],
                             mode='markers', marker={'color': 'red'}))

    fig = go.Figure(data=data)
    fig.update_layout(
        scene=dict(
            xaxis=dict(tickmode="linear", range=[0, max_x], linewidth=1),
            yaxis=dict(tickmode="linear", range=[0, max_y], linewidth=1),
            zaxis=dict(tickmode="linear", range=[0, max_z], linewidth=1),
        ))
    fig.show()


if __name__ == '__main__':
    main()
