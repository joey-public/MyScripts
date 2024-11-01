import numpy as np

class Rect():
    def __init__(self, x0:int, y0:int, w:int, h:int):
        if w < 0:
            return np.zeros(shape=(2,2))
        if h < 0:
            return np.zeros(shape=(2,2))
        self._data = np.array([[x0, x0+w], [y0, y0+h]], dtype=int)
    #mutation functions that can change the state of the rectangle. 
    def __translate(self, dx, dy)->None:
        self.data[0,:] += dx  
        self.data[1,:] += dy 
    def __applyXform(self, xform:np.array)->None:
        if not(xform.shape == (2,2)): 
            return 
        self.data = np.matmul(xform, self.data)
    #read only properties. The properties cannot be altered directly. Only updated by xforming the data.
    def getData(self)->np.array:
        return self._data
    raw_data = property(getData, None, None, 'The raw point data of the rectangle. Points are Stored Column Wise.')
    def getX0(self)->int:
        return min(self._data[0,0], self._data[0,1])
    x0 = property(getX0, None, None, 'The left-most x value of the rectangle.') 
    def getY0(self)->int:
        return min(self._data[1,0], self._data[1,1])
    y0 = property(getY0, None, None, 'The bottom-most y value of the rectangle.')
    def getX1(self)->int:
        return max(self._data[0,0], self._data[0,1])
    x1 = property(getX1, None, None, 'The right-most x value of the rectangle.')
    def getY1(self)->int:
        return max(self._data[1,0], self._data[1,1])
    y1 = property(getY1, None, None, 'The top-most y value of the rectangle.') 
    def getW(self)->int:
        return self.x1()-self.x0()
    w = property(getW(), None, None, 'The width of the rectangle.')
    def getH(self)->int:
        return self.y1()-self.y0()
    h = property(getH(), None, None, 'The height of the rectangle')
    def getBl(self)->tuple:
        return (self.x0, self.y0)
    bl = property(getBl(), None, None, 'The bottom left point (x0,y0) of the rectangle.')
    def getBr(self)->tuple:
        return (self.x1, self.y0)
    br = property(getBr(), None, None, 'The bottom right point (x1,y0) of the rectangle.')
    def getTl(self)->tuple:
        return (self.x0, self.y1)
    tl = property(getTl(), None, None, 'The top left point (x0,y1) of the rectangle.')
    def getTr(self)->tuple:
        return (self.x1, self.y1)
    tr = property(getTl(), None, None, 'The top right point (x1,y1) of the rectangle.')
    def getCenterX(self)->float:
        return float(self.x0) + float(self.x1-self.x0)/2.0
    cx = property(getCenterX, None, None, 'The center x-axis of the rectangle.')
    def getCenterY(self)->float:
        return float(self.y0) + floar(self.y1-self.y0)/2.0
    cy = property(getCenterY, None, None, 'The center y-axis of the rectangle.')
          


if __name__=='__main__':
    r0 = Rect(1,3,4,6)
    print(r0)

