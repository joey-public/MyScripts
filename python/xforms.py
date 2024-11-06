import numpy as np
from Point2D import _Shape

ROT90_XFORM = np.array([[0, -1],
                      [1,  0] ])
FLIP_H_XFORM = np.array([[-1,  0],
                         [ 0,  1] ])
FLIP_V_XFORM = np.array([[ 1,  0],
                         [ 0, -1] ])
FLIP_HV_XFORM = np.array([[-1,  0],
                         [ 0, -1] ])

def xform(s:_Shape, xform:np.ndarray)->None:
    data = s.getData()
    s.updateData(np.matmul(xform, data))
def translate(s, dx, dy)->None:
    d = np.array([dx,dy])
    d.shape = (2,1)
    s.updateData(s.getData() + d)
def moveTo(s:_Shape, xpos, ypos): 
    pos = np.array([xpos, ypos])
    pos.shape = (2,1)
    d = pos - s.getPos()
    s.updateData(s.getData() + d)
def scale(s:_Shape, sf)->None: 
    s.updateData(s.getData()*sf)
def stretch(s:_Shape, sx, sy)->None:
    x, y = (s.getPos()[0,0], s.getPos()[1,0])
    s.moveTo(0,0)
    xf = np.array([ [sx, 0], 
                    [0, sy] ])
    s.xform(xf)
    s.moveTo(x,y)
def rot90(s:_Shape, xpos, ypos)->None:
    s.translate(-xpos,-ypos)
    s.xform(ROT90_XFORM)
    s.translate(xpos, ypos)
def flip_h(s:_Shape)->None:
    x, y = (s.getPos()[0,0], s.getPos()[1,0])
    s.translate(-dx, -dy)
    s.xform(FLIP_H_XFORM)
    s.translate(dx, dy)
def flip_v(s:_Shape)->None:
    x, y = (s.getPos()[0,0], s.getPos()[1,0])
    s.translate(-dx, -dy)
    s.xform(FLIP_V_XFORM)
    s.translate(dx, dy)
def flip(s:_Shape, flip_h:bool, flip_v:bool)->None:
    if not(flip_h) and not(flip_v): return 
    x, y = (s.getPos()[0,0], s.getPos()[1,0])
    s.translate(-dx, -dy)
    if flip_h and flip_v:
       s.xform(FLIP_HV_XFORM)
    elif flip_h:
       s.xform(FLIP_H_XFORM)
    else:
       s.xform(FLIP_V_XFORM)
    s.translate(dx, dy)
