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
    _precision = 6#round to 6 decimals
    def getData(self)->np.ndarray: pass
    def updateData(self, new_data:np.array)->None: pass
    def getPos(self)->np.ndarray: pass
    def xform(self, xform:np.ndarray)->None:
        data = self.getData()
        new_data = np.matmul(xform, data)
        self.updateData(np.round(new_data, self._precision))
    def scale(self, sf)->None: 
        self.updateData(self.getData()*sf)
    def translate(self, dx, dy)->None:
        d = np.array([dx,dy])
        d.shape = (2,1)
        self.updateData(self.getData() + d)
    def moveTo(self, xpos, ypos): 
        pos = np.array([xpos, ypos])
        pos.shape = (2,1)
        d = pos - self.getPos()
        new_data = self.getData() + d
        self.updateData(np.round(new_data, self._precision))
    def stretch(self, sx, sy)->None:
        x, y = (self.getPos()[0,0], self.getPos()[1,0])
        self.moveTo(0,0)
        xf = np.array([ [sx, 0], 
                        [0, sy] ])
        self.xform(xf)
        self.moveTo(x,y)
    def rot90(self, xpos, ypos)->None:
        self.translate(-xpos,-ypos)
        self.xform(ROT90_XFORM)
        self.translate(xpos, ypos)
#    def flip_h(self)->None:
#        x, y = (self.getPos()[0,0], self.getPos()[1,0])
#        self.moveTo(0, 0)
#        self.xform(FLIP_H_XFORM)
#        self.moveTo(x, y)
#    def flip_v(self)->None:
#        x, y = (self.getPos()[0,0], self.getPos()[1,0])
#        self.moveTo(0, 0)
#        self.xform(FLIP_V_XFORM)
#        self.moveTo(x, y)
