import numpy as np
from Point2D import Point2D
   
class Vec2D:
    def __init__(self, p0:Point2D, p1:Point2D):
        self._data = np.hstack((p0, p1)) 
    def __eq__(self, other):
        return self.p0.x==other.p0.x and self.p0.y==other.p0.y and self.p1.x==other.p1.x and self.p1.y==other.p1.y
    def __hash__(self,other):
        return hash((self.p0.x, self.p0.y, self.p1.x, self.p1.y))
    def __getp0(self):
        return self._data[0]
    p0 = property(__getp0, None, None, '')
    def __getp1(self):
        return self._data[1]
    p1 = property(__getp1, None, None, '')
    def __getRawData(self):
        return np.hstack((self.p0.raw_data, self.p1.raw_data))
    raw_data = property(__getRawData, None, None, '')
