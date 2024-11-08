import numpy as np
from Shape import _Shape
from Rect import Rect
from Point2D import Point2D

class RectArray(_Shape):
    def __init__(self, r0:Rect, x_pitch, y_pitch, 
                       nrows:int, ncols:int, dt=np.float64):
        assert x_pitch>=0, 'RectArrya has not been tested with negative x pitches.'
        assert y_pitch>=0, 'RectArrya has not been tested with negative y pitches.'
        assert nrows>0, f'RectArray must have at lease 1 row. you passed {nrows}.'
        assert ncols>0, f'RectArray must have at lease 1 col. you passed {ncols}.'
        assert r0.getData().dtype == dt, 'RectArray r0 dtype does not match dt. This is a know bug that needs fixing.'
        self._r0 = Rect(r0.x0, r0.y0, r0.w, r0.h)
        self._pitch = Point2D(x_pitch, y_pitch, dt)
        self.nrows = nrows
        self.ncols = ncols
    def __eq__(self, other):
        if not(type(other)==type(self)): 
            return False
        return self.r0 == other.r0 and self._pitch==other._pitch and self.nrows==other.nrows and self.ncols==other.ncols
    def __hash__(self, other):
        return hash((self._r0, self._pitch, self.nrows, self.ncols))
    #public functions
    def getData(self):
        return self.r0.getData()
    def updateData(self, new_data:np.ndarray)->None:
        assert new_data.shape == (2,2), 'Rect Array: UpdateData takes new_data arg with shape (2,2) [[x0,x1][y0,y1]].'
        self.r0.updateData(new_data)
    def getPos(self):
        return self.r0.getPos()
    def scale(self, sf)->None: #overides scale from _Shape class
        super().scale(sf)
        self.pitch.scale(sf)
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
        h = (self.nrows-1)*self.pitch.y + self.r0.h
        return Rect(x0, y0, w, h) 
    r0 = property(__getR0, None, None, 'The bottom Left Rect in the Array.') 
    pitch = property(__getPitch, None, None, 'The x-pitch of the Array.')
    dx = property(__getDeltaX, None, None, 'The x-spacing of the Array.')
    dy = property(__getDeltaY, None, None, 'The y-spacinf of the Array.')
    bbox = property(__getBbox, None, None, 'The bbox of the Array.')
