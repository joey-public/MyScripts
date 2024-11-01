import numpy as np

class Rect():
    def __init__(self, x0:int, y0:int, w:int, h:int):
        if w < 0:
            return np.zeros(shape=(2,2))
        if h < 0:
            return np.zeros(shape=(2,2))
        self._data = np.array([[x0, x0+w], [y0, y0+h]], dtype=int)
    def getX0(self)->int:
        return min(self._data[0,0], self._data[0,1])
    def setX0(self)->None: pass
    def delX0(self)->None: pass
    x0 = property(getX0, setX0, delX0, 'The left-most x value of the rectangle.') 

    def getY0(self)->int:
        return min(self._data[1,0], self._data[1,1])
    def setY0(self)->None: pass
    def delY0(self)->None: pass
    y0 = property(getY0, setY0, delY0, 'The bottom-most y value of the rectangle.')

    def getX1(self)->int:
        return max(self._data[0,0], self._data[0,1])
    def setX1(self)->None: pass
    def delX1(self)->None: pass
    x1 = property(getX1, setX1, delX1, 'The right-most x value of the rectangle.')

    def getY1(self)->int:
        return max(self._data[1,0], self._data[1,1])
    def setY1(self)->None: pass
    def delY1(self)->None: pass
    y1 = property(getY1, setY1, delY1, 'The top-most') 

    def w(self)->int:
        return self.x1()-self.x0()
    def h(self)->int:
        return self.y1()-self.y0()

    def __translate(self, dx, dy)->None:
        self.data[0,:] += dx  
        self.data[1,:] += dy 
    def __applyXform(self, xform:np.array)->None:
        if not(xform.shape == (2,2)): 
            return 
        self.data = np.matmul(xform, self.data)
#        return self


if __name__=='__main__':
    r0 = Rect(1,3,4,6)
    print(r0)
    print(r0._data)
    print(r0.x0)
    print(r0.y0)
    print(r0.x1)
    print(r0.y1)
