import numpy as np
import math

ROT90_XFORM = np.array([[0, -1],
                      [1,  0] ])
FLIP_H_XFORM = np.array([[-1,  0],
                         [ 0,  1] ])
FLIP_V_XFORM = np.array([[ 1,  0],
                         [ 0, -1] ])
FLIP_HV_XFORM = np.array([[-1,  0],
                         [ 0, -1] ])
class _Shape:
    def getData(self)->np.ndarray: pass
    def updateData(self, new_data:np.array)->None: pass
    def getAnchor(self)->tuple: pass
    def xform(self, xform:np.ndarray)->None:
        data = self.getData()
        self.updateData(np.matmul(xform, data))
    def translate(self, dx, dy)->None:
        d = np.array([dx,dy])
        d.shape = (2,1)
        self.updateData(self.getData() + d)
    def moveTo(self, xpos, ypos): 
        pos = np.array([xpos, ypos])
        pos.shape = (2,1)
        d = pos - self.getAnchor()
        self.updateData(self.getData() + d)
    def scale(self, sf)->None: 
        self.updateData(self.getData()*sf)
    def stretch(self, sx, sy)->None:
        x, y = (self.x0, self.y0)
        self.moveTo(0,0)
        xf = np.array([ [sx, 0], 
                           [0,  sy] ])
        self.xform(xf)
        self.moveTo(x,y)
    def rot90(self, xpos, ypos)->None:
        self.translate(-xpos,-ypos)
        self.xform(ROT90_XFORM)
        self.translate(xpos, ypos)
    def flip(self, flip_h:bool, flip_v:bool)->None:
        if not(flip_h) and not(flip_v): return 
        dx, dy = (self.x0, self.y0)
        self.translate(-dx, -dy)
        if flip_h and flip_v:
            self.xform(FLIP_HV_XFORM)
        elif flip_h:
            self.xform(FLIP_H_XFORM)
        else:
            self.xform(FLIP_V_XFORM)
        self.translate(dx, dy)
            
#This wont work becasue of how I defined the rectangle.
#    def rotate(self, angle, xpos, ypos)->None:
#        self.translate(-xpos,-ypos)
#        xform = np.array([ [math.cos(angle), -1*math.sin(angle)],
#                           [math.sin(angle),  math.cos(angle)] ], dtype = np.float64)
#        self.xform(xform)
#        self.translate(xpos, ypos)
