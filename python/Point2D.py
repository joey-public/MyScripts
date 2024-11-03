import numpy as np

class Point2D:
    def __init__(self, x:np.int64, y:np.int64):
        self._data = np.array([x,y], dtype=np.int64)
        self._data.shape = (2,1)
    def __eq__(self, other):
        return (self.x == other.x) and (self.y == self.y)
    def __hash__(self):
        return hash((self.x, self.y))
    ##read only properties
    def __getX(self):
        return self._data[0][0]
    x = property(__getX, None, None, '')
    def __getY(self):
        return self._data[1][0]
    y = property(__getY, None, None, '')
