import random
import FreeCAD
from FreeCAD import Base

values = App.ActiveDocument.getObjectsByLabel('Values')[0]
sketch = App.ActiveDocument.getObjectsByLabel('Layer1')[0]


# random.seed(10)


vPoints = [None] * values.noPoints

for i in range(values.noPoints):
	vPoints[i] = sketch.addGeometry(Part.Point(App.Vector(0, 0)))
	sketch.addConstraint(Sketcher.Constraint('DistanceX', vPoints[i], 1, App.Units.Quantity(str(random.random() * values.maxX))))
	sketch.addConstraint(Sketcher.Constraint('DistanceY', vPoints[i], 1, App.Units.Quantity(str(random.random() * values.maxY))))
print(vPoints)