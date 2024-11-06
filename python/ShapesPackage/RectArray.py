import numpy as np
from Shape import _Shape
from Rect import Rect
from Point2D import Point2D

class RectArray(_Shape):
    def __init__(self, r0:Rect, x_pitch, y_pitch, nrows:int, ncols:int, data_type=np.float64):
        self._r0 = r0
        self._pitch = Point2D(x_pitch, y_pitch)
        self.nrows = nrows
        self.ncols = ncols
    def __eq__(self, other):
        return self.r0 == other.r0 and self._pitch==other._pitch 
    #Properties
    def __getR0(self):
        return self._r0 
    def __getPitch(self):
        return self._pitch
    def __getDeltaX(self):
        return self.pitch.x - self.r0.w
    def __getDeltaY(self):
        return self.pitch.y - self.r0.h
    def __getBbox(self):
        x0 = self.r0.x0
        y0 = self.r0.y0
        w = (self.ncols-1)*self.pitch.x + self.r0.w
        h = (self.nrows-1)*self.pitch.x + self.r0.w
        return Rect(x0, y0, w, h) 
    r0 = property(__getR0, None, None, 'The bottom Left Rect in the Array.') 
    pitch = property(__getPitch, None, None, 'The x-pitch of the Array.')
    dx = property(__getDeltaX, None, None, 'The x-spacing of the Array.')
    dy = property(__getDeltaY, None, None, 'The y-spacinf of the Array.')
    bbox = property(__getBbox, None, None, 'The bbox of the Array.')
    #public functions
    def getData(self):
        return self._r0.getData()
    def updateData(self, new_data:np.ndarray)->None:
        self.r0.updateData(new_data)
    def getPos(self):
        return self.r0.getPos()
