from math import sin, tan, atan, radians, degrees
from typing import final
import random

import plotly.graph_objects as go
import numpy as np

from Point import Point, pointdistance

THETA:final = 30
MEW:final = 0.5
DELTA:final = (180 - THETA) / 2

NOPOINTS:final = 2


def getTriangleVertices(p: Point, scale: float):
    opposite = scale / 2
    height = opposite / tan(radians(THETA / 2))

    # Points are returned (Top Point, Left Point, Right Point) of triangle
    return [Point(p.x, p.y + MEW * height, p.z),
            Point(p.x - opposite, p.y - height + MEW * height, p.z),
            Point(p.x + opposite, p.y - height + MEW * height, p.z)]


def pointsToScatter(pointarray, formTriangle: bool):
    xarray = [point.x for point in pointarray]
    yarray = [point.y for point in pointarray]
    zarray = [point.z for point in pointarray]
    if formTriangle:
        xarray.append(pointarray[0].x)
        yarray.append(pointarray[0].y)
        zarray.append(pointarray[0].z)
    return [xarray, yarray, zarray]

def calculateMeetingSize(p1: Point, p2: Point):

    # TODO: if im oberen sektor is anders berechnen
    #       return y difference / height
    dist = pointdistance(p1, p2)
    alpha = degrees(atan(abs(p1.y - p2.y) / abs(p1.x - p2.x)))
    return dist * sin(radians(180 - alpha - DELTA)) / sin(radians(DELTA))


def main():
    size = 1

    points = [Point(np.random.uniform(0, 10), np.random.uniform(0, 10), 0.5) for _ in range(NOPOINTS)]
    triangles = [getTriangleVertices(points[i], size) for i in range(NOPOINTS)]

    scatter_triangles = []
    for triangle in triangles:
        scatter_triangles.append(pointsToScatter(triangle, True))

    # TODO: insert loop und alles andere
    newsize = calculateMeetingSize(points[0], points[1])

    triangles = [getTriangleVertices(points[i], newsize) for i in range(NOPOINTS)]
    for triangle in triangles:
        scatter_triangles.append(pointsToScatter(triangle, True))

    scatter_points = pointsToScatter(points, False)

    colors = ["#%06x" % random.randint(0, 0xFFFFFF) for _ in range(NOPOINTS)]
    data = [go.Scatter3d(x=scatter_triangles[i][0], y=scatter_triangles[i][1], z=scatter_triangles[i][2],
                         mode='lines', line={'color': colors[i % NOPOINTS]}) for i in range(len(scatter_triangles))]
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
