from typing import Final
import numpy as np
import Draft, Part, Sketcher

numberOfPoints = 10

maxX = 100
maxY = 50

slope = "30 deg"

theta = "15 deg"

doc = App.activeDocument()


class Triangle:

    def __init__(self, sketch):
        self.triangle_sketch = sketch
        self.origin = None
        self.thetaLine = None
        self.height = None
        self.base = None
        self.rightLeg = None
        self.leftLeg = None
        self.rightPoint = None
        self.leftPoint = None
        self.topPoint = None
        self.totalHeightConstraint = None

    def gen_triangle(self, is_help_geometry):
        # Generate Base Triangle
        # Draw Points
        self.topPoint = self.triangle_sketch.addGeometry(Part.Point(App.Vector(0, 1, 0)))
        self.leftPoint = self.triangle_sketch.addGeometry(Part.Point(App.Vector(-1, -1, 0)))
        self.rightPoint = self.triangle_sketch.addGeometry(Part.Point(App.Vector(1, -1, 0)))
        # Draw Origin
        self.origin = self.triangle_sketch.addGeometry(Part.Point(App.Vector(0, 0, 0)))

        # Draw Lines
        self.leftLeg = self.triangle_sketch.addGeometry(Part.LineSegment(App.Vector(-1, -1, 0),
                                                            App.Vector(0, 1, 0)), is_help_geometry)
        self.rightLeg = self.triangle_sketch.addGeometry(Part.LineSegment(App.Vector(1, 1, 0),
                                                                     App.Vector(0, -1, 0)), is_help_geometry)
        self.base = self.triangle_sketch.addGeometry(Part.LineSegment(App.Vector(-1, -1, 0),
                                                            App.Vector(1, -1, 0)), is_help_geometry)
        self.height = self.triangle_sketch.addGeometry(Part.LineSegment(App.Vector(0, -1, 0),
                                                              App.Vector(0, 1, 0)), True)
        self.thetaLine = self.triangle_sketch.addGeometry(Part.LineSegment(App.Vector(-1, -1, 0),
                                                                   App.Vector(0, 0, 0)), True)

        # Add Coincidences
        self.triangle_sketch.addConstraint(Sketcher.Constraint('Coincident', self.leftPoint, 1, self.leftLeg, 1))
        self.triangle_sketch.addConstraint(Sketcher.Constraint('Coincident', self.topPoint, 1, self.leftLeg, 2))

        self.triangle_sketch.addConstraint(Sketcher.Constraint('Coincident', self.rightPoint, 1, self.rightLeg, 1))
        self.triangle_sketch.addConstraint(Sketcher.Constraint('Coincident', self.topPoint, 1, self.rightLeg, 2))

        self.triangle_sketch.addConstraint(Sketcher.Constraint('Coincident', self.leftPoint, 1, self.base, 1))
        self.triangle_sketch.addConstraint(Sketcher.Constraint('Coincident', self.rightPoint, 1, self.base, 2))

        self.triangle_sketch.addConstraint(Sketcher.Constraint('Coincident', self.topPoint, 1, self.height, 2))

        self.triangle_sketch.addConstraint(Sketcher.Constraint('Coincident', self.leftPoint, 1, self.thetaLine, 1))
        self.triangle_sketch.addConstraint(Sketcher.Constraint('Coincident', self.origin, 1, self.thetaLine, 2))

        # Add other Constraints
        self.triangle_sketch.addConstraint(Sketcher.Constraint('Equal', self.leftLeg, self.rightLeg))
        self.triangle_sketch.addConstraint(Sketcher.Constraint('Horizontal', self.base))
        self.triangle_sketch.addConstraint(Sketcher.Constraint('Vertical', self.height))
        self.triangle_sketch.addConstraint(Sketcher.Constraint('PointOnObject', self.height, 1, self.base))
        self.triangle_sketch.addConstraint(Sketcher.Constraint('PointOnObject', self.origin, 1, self.height))

        self.triangle_sketch.addConstraint(
            Sketcher.Constraint('Angle', self.leftLeg, 2, self.height, 2, App.Units.Quantity(slope)))
        # Place at certain point below origin
        self.triangle_sketch.addConstraint(
            Sketcher.Constraint('Angle', self.base, 1, self.thetaLine, 1, App.Units.Quantity(theta)))

    def fix_triangle(self, x, y):
        if x == 0 & y == 0:
            self.triangle_sketch.addConstraint(Sketcher.Constraint('Coincident', self.origin, 1, -1, 1))
        else:
            self.triangle_sketch.addConstraint(Sketcher.Constraint('DistanceX', self.origin, 1, App.Units.Quantity(str(x) + " mm")))
            self.triangle_sketch.addConstraint(Sketcher.Constraint('DistanceY', self.origin, 1, App.Units.Quantity(str(y) + " mm")))

    def move_triangle(self, v_point):
        # Fix height in order to avoid the triangle to be flipped
        height_constraint = self.triangle_sketch.addConstraint(Sketcher.Constraint(
            'DistanceY', self.height, 1, self.height, 2, self.triangle_sketch.Geometry[self.height].length()))

        # Place at specific point
        self.triangle_sketch.addConstraint(Sketcher.Constraint('Coincident', self.origin, 1, v_point.sketchNumber, 1))

        # Remove height_constraint
        self.triangle_sketch.delConstraint(height_constraint)

    def set_reference(self, reference_base):
        # Set Equal To Reference Geometry
        self.triangle_sketch.addConstraint(Sketcher.Constraint('Equal', self.base, reference_base))


class VPoint:
    draftPoint = None
    sketchNumber = 0
    X: Final
    Y: Final
    triangle = None

    def __init__(self):
        self.X = np.random.uniform(low=0, high=maxX)
        self.Y = np.random.uniform(low=0, high=maxY)


# Generate Points as a draft object
vPoints = np.empty(numberOfPoints, dtype=VPoint)

voronoiPart = doc.addObject('App::Part', 'VoronoiPart')

pointGroup = doc.addObject('App::DocumentObjectGroup', 'PointGroup')
doc.PointGroup.Label = 'VoronoiPoints'

pointGroup.adjustRelativeLinks(voronoiPart)
voronoiPart.addObject(pointGroup)

for i in range(numberOfPoints):
    vPoints[i] = VPoint()
    vPoints[i].draftPoint = Draft.make_point(str(vPoints[i].X) + " mm", str(vPoints[i].Y) + " mm", 0,
                                             name="VPoint_" + str(i))
    vPoints[i].draftPoint.adjustRelativeLinks(pointGroup)
    pointGroup.addObject(vPoints[i].draftPoint)

doc.recompute()

voronoiSketch = doc.addObject("Sketcher::SketchObject", "VoronoiSketch")
voronoiSketch.Placement = App.Placement(App.Vector(0, 0, 0), App.Rotation(0, 0, 0, 1))
voronoiSketch.adjustRelativeLinks(pointGroup)
pointGroup.addObject(voronoiSketch)

baseTriangle = Triangle(voronoiSketch)
baseTriangle.gen_triangle(True)
baseTriangle.fix_triangle(0, 0)

for i in range(numberOfPoints):  # there must be a more elegant solution
    voronoiSketch.addExternal(vPoints[i].draftPoint.Label, "Vertex1")
    vPoints[i].sketchNumber = -3 - i
    doc.recompute()

    vPoints[i].triangle = Triangle(voronoiSketch)
    vPoints[i].triangle.gen_triangle(False)
    vPoints[i].triangle.move_triangle(vPoints[i])
    vPoints[i].triangle.set_reference(baseTriangle.base)
