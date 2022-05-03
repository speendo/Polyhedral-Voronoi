from math import tan, atan, radians
import random

import plotly.graph_objects as go
# import numpy as np

from dataclasses import dataclass


@dataclass
class Point:
    x: float
    y: float
    z: float


def getTriangleVertices(p: Point, size: float):
    THETA = 30
    MEW = 0.5

    opposite = size/2
    height = opposite / tan(radians(THETA / 2))
    #opposite = tan(radians(THETA / 2)) * height

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



def main():
    HEIGHT = 1
    NOPOINTS = 1

    points = [Point(random.random()*10, random.random()*10, 0.5) for _ in range(NOPOINTS)]
    triangles = [getTriangleVertices(points[i], HEIGHT) for i in range(NOPOINTS)]


    scattertriangles = []
    for triangle in triangles:
        scattertriangles.append(pointsToScatter(triangle, True))
    scatterpoints = pointsToScatter(points, False)

    data = [go.Scatter3d(x=scattertriangles[i][0], y=scattertriangles[i][1], z=scattertriangles[i][2], mode='lines') for i in range(
        len(triangles))]
    data.append(go.Scatter3d(x=scatterpoints[0], y=scatterpoints[1], z=scatterpoints[2], mode='markers'))

    fig = go.Figure(data=data)
    fig.update_yaxes(
        scaleanchor="x",
        scaleratio=1,
    )
    fig.show()


if __name__ == '__main__':
    main()
