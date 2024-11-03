import numpy as np
from Point2D import Point2D
   
class Vec2D:
    def __init__(self, tip:Point2D, tail:Point2D):
        self._data = np.hstack((tip,tail)) 
    def __eq__(self, other):
        return self.tip.x==other.tip.x and self.tip.y==other.tip.y and self.tail.x==other.tail.x and self.tail.y==other.tail.y
    def __hash__(self,other):
        return hash((self.tip.x, self.tip.y, self.tail.x, self.tail.y))
    def __getTip(self):
        return self._data[0]
    tip = property(__getTip, None, None, '')
    def __getTail(self):
        return self._data[1]
    tail = property(__getTail, None, None, '')
