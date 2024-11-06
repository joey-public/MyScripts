import numpy as np
from Shape import _Shape


class Point2D(_Shape):
    def __init__(self, x, y, dtype=np.int64):
        self._data = np.array([x,y], dtype=np.int64)
        self._data.shape = (2,1)
    def __eq__(self, other):
        return (self.x == other.x) and (self.y == self.y)
    def __hash__(self):
        return hash((self.x, self.y))
    ##public functions
    def updateData(self, new_data):
        self._data = new_data
    def getData(self):
        return self._data
    def getPos(self):
        return self._data
    ##read only properties
    def __getX(self):
        return self._data[0][0]
    x = property(__getX, None, None, 'y value of the Point2D.')
    def __getY(self):
        return self._data[1][0]
    y = property(__getY, None, None, 'x valie of the Point2D.')
