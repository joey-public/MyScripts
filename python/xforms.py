import numpy as np
from Point2D import _Shape

def xform(shape:_Shape, xform:np.array):
    data = shape.getData
    shape.updateData(np.matmul(xform, data))

def scale(shape:_Shape, sf):
    shape.updateData(sf*shape.getData())

def translate(shape:_Shape, dx, dy):
    d = np.array([dx,dy])
    d.shape = (2,1)
    shape.updateData(shape.getData() + d)

