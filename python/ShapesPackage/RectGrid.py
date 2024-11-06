import numpy as np

from Shape import _Shape
from Point2D import Point2D
from Rect import Rect
from RectArray import RectArray
import RectMath as rm

class RectGrid(_Shape):
    def __init__(self, h_rects:RectArray, v_rects:RectArray):
        assert h_rects.ncols==1, 'RectGrid.h_rects must have 1 col.'
        assert v_rects.nrows==1, 'RectGrid.v_rects must have 1 col.'
        assert rm.rect_overlaps_rect(h_rects.r0, v_rects.r0), 'REctGrid h_rect.r0 and v_rect.r0 must overlapREctGrid h_rect.r0 and v_rect.r0 must overlap.'
        self._h_rects = h_rects
        self._v_rects = v_rects
    def __eq__(self, other):
        return self.h_rects==other.h_rects and self.v_rects==other.v_rects and self.bbox==other.bbox
    def __getHRects(self)->RectArray:
        return self._h_rects
    def __getVRects(self)->RectArray:
        return self._v_rects
    def __getBbox(self)->RectArray:
        x0 = min(self.h_rects.r0.x0, self.v_rects.r0.x0)
        y0 = min(self.h_rects.r0.y0, self.v_rects.r0.y0)
        x1 = max(self.h_rects.r0.x1, self.v_rects.r0.x1)
        y1 = max(self.h_rects.r0.y1, self.v_rects.r0.y1)
        return Rect(x0, y0, x1-x0, y1-y0)
    def __getOlapRects(self)->RectArray:
        r0 = rm.get_overlap_rect(self.h_rects.r0, self.v_rects.r0)
        pitch = Point2D(self.v_rects.pitch.x, self.h_rects.pitch.y)
        return RectArray(r0, pitch.x, pitch.y, self.nrows, self.ncols)
    def __getRows(self):
        return self.h_rects.nrows
    def __getCols(self):
        return self.v_rects.ncols
    h_rects = property(__getHRects, None, None, '')
    v_rects = property(__getVRects, None, None, '')
    bbox = property(__getBbox, None, None, '')
    o_rects = property(__getOlapRects, None, None, '')
    nrows = property(__getRows, None, None, '')
    ncols = property(__getCols, None, None, '')
    def getData(self)->np.ndarray:
        d = np.hstack((self.h_rects.getData(), self.v_rects.getData()))
        return np.hstack((self.h_rects.getData(), self.v_rects.getData()))
    def updateData(self, new_data:np.ndarray)->None:
        if not(new_data.shape == (2,4)): return 
        h_rect_data = new_data[0:2, 0:2]
        v_rect_data = new_data[0:2, 2:4]
        self._h_rects.updateData(h_rect_data)
        self._v_rects.updateData(v_rect_data)
    def getPos(self):
        return self.bbox.getPos()
    def stretch(self, sx, sy)->None:
        self._h_rects.stretch(sx, 1)
        self._v_rects.stretch(1, sy)
