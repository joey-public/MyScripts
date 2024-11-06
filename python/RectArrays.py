import numpy as np
from Rect import Rect
from Point2D import Point2D

class RectArray():
    def __init__(self, r0:Rect, x_pitch, y_pitch, nrows:int, ncols:int, data_type=np.float64):
        self._bl_rect = r0
        self._pitch = Point2D(x_pitch, y_pitch)
        self.nrows = nrows
        self.ncols = ncols
    def __eq__(self, other):
        return self.bl_rect==other.bl_rect and self.x_pitch==other.x_pitch and self.y_pitch==other.y_pitch
    def __getBlRect(self):
        return self._bl_rect
    def __getPitch(self):
        return self._pitch
    def __getDeltaX(self):
        return self.pitch.x - self.bl_rect.w
    def __getDeltaY(self):
        return self.pitch.y - self.bl_rect.h
    bl_rect = property(__getBlRect, None, None, 'The bottom Left Rect in the Array.') 
    pitch = property(__getPitch, None, None, 'The x-pitch of the Array.')
    dx = property(__getDeltaX, None, None, '')
    dy = property(__getDeltaY, None, None, '')
    
