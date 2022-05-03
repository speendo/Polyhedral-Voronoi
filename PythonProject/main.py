from math import sin, tan, atan, radians, degrees
import random

import plotly.graph_objects as go
import numpy as np

from dataclasses import dataclass



from Point import Point, distance

THETA = 30
MEW = 0.5
DELTA = (180-THETA)/2

NOPOINTS = 2


def getTriangleVertices(p: Point, size: float):

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

    size = 1

    points = [Point(random.random()*10, random.random()*10, 0.5) for _ in range(NOPOINTS)]
    triangles = [getTriangleVertices(points[i], size) for i in range(NOPOINTS)]

    scattertriangles = []
    for triangle in triangles:
        scattertriangles.append(pointsToScatter(triangle, True))


    dist = distance(points[0], points[1])
    print(abs(points[0].y - points[1].y) / abs(points[0].x - points[1].x))
    alpha = degrees(atan(abs(points[0].y - points[1].y) / abs(points[0].x - points[1].x)))
    print(alpha)
    newsize = dist * sin(radians(180-alpha-DELTA)) / sin(radians(DELTA))

    print(newsize)

    triangles = [getTriangleVertices(points[i], newsize) for i in range(NOPOINTS)]
    for triangle in triangles:
        scattertriangles.append(pointsToScatter(triangle, True))


    scatterpoints = pointsToScatter(points, False)

    data = [go.Scatter3d(x=scattertriangles[i][0], y=scattertriangles[i][1], z=scattertriangles[i][2], mode='lines') for i in range(
        len(scattertriangles))]
    data.append(go.Scatter3d(x=scatterpoints[0], y=scatterpoints[1], z=scatterpoints[2], mode='markers'))


    fig = go.Figure(data=data)
    fig.update_layout(
        scene=dict(
            xaxis=dict(tickmode="linear", range=[-5,15], linewidth=1),
            yaxis=dict(tickmode="linear", range=[-5,15], linewidth=1),
            zaxis=dict(tickmode="linear", range=[-5,15], linewidth=1),
        ))
    fig.show()


if __name__ == '__main__':
    main()
