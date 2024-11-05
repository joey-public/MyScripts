import numpy as np

class _Shape:
    def updateData(): pass
    def getData(): pass
    #def updateDataType(): pass
    #def getDataType(): pass

class Point2D(_Shape):
    def __init__(self, x, y, dtype=np.int64):
        self._data = np.array([x,y], dtype=np.int64)
        self._data.shape = (2,1)
    def __eq__(self, other):
        return (self.x == other.x) and (self.y == self.y)
    def __hash__(self):
        return hash((self.x, self.y))
    ##public functions
    def updateData(self, x, y):
        self._data[0,0] = x
        self._data[0,1] = y
    def getData(self):
        return self._data
    ##read only properties
    def __getX(self):
        return self._data[0][0]
    x = property(__getX, None, None, 'y value of the Point2D.')
    def __getY(self):
        return self._data[1][0]
    y = property(__getY, None, None, 'x valie of the Point2D.')

class Rect(_Shape):
    def __init__(self, x0, y0, w, h, dtype=np.int64):
        self._data = np.array([[x0, x0+w], [y0, y0+h]], dtype=np.int64)
    def __eq__(self, other):
        return (self.x0==other.x0) and (self.y0==other.y0) and (self.x1==other.x1) and (self.y1==other.y1)
    #private funcs
    def __getMinX(self, data:np.array):
        return min(data[0,0], data[0,1])
    def __getMaxX(self, data:np.array):
        return max(data[0,0], data[0,1])
    def __getMinY(self, data:np.array):
        return min(data[1,0], data[1,1])
    def __getMaxY(self, data:np.array):
        return max(data[1,0], data[1,1])
    #Public functions
    def updateData(self, new_data:np.array):
        if new_data.shape != (2,2):
            return 
        x0 = __getMinX(new_data)
        y0 = __getMinY(new_data)
        x1 = __getMaxX(new_data)
        y1 = __getMaxY(new_data)
        self._data[0,0] = x0
        self._data[1,0] = y0
        self._data[0,1] = x1
        self._data[1,1] = y1
    def getData(self):
        return self._data
    #private property getters
    def _getX0(self):
        data = self._data[0,0]
        assert data == self.__getMinX(self._data), f'rect data misformatted, x0 is not min x.'
        return data
    def _getX1(self):
        data = self._data[0,1]
        assert data == self.__getMaxX(self._data), f'rect data misformatted, x1 is not max x1.'
        return data
    def _getY0(self):
        data = self._data[1,0]
        assert data == self.__getMinY(self._data), 'rect data misformatted, y0 is not min y.'
        return data
    def _getY1(self):
        data = self._data[1,1]
        assert data == self.__getMaxY(self._data), f'rect data misformatted, y1 is not max y.'
        return data
    def _getW(self):
        return self.x1-self.x0
    def _getH(self):
        return self.y1-self.y0
    def _getBl(self)->Point2D:
        return Point2D(self.x0, self.y0)
    def _getBr(self)->Point2D:
        return Point2D(self.x1, self.y0)
    def _getTl(self)->Point2D:
        return Point2D(self.x0, self.y1)
    def _getTr(self)->Point2D:
        return Point2D(self.x1, self.y1)
    def _getCenterX(self)->int:
        return int(self.x0 + self.w/2)
    def _getCenterY(self)->int:
        return int(self.y0 + self.h/2)
    def _getCenter(self)->Point2D:
        return Point2D(self.cx, self.cy)
    def _getCl(self)->Point2D:
        return Point2D(self.x0, self.cy)
    def _getCr(self)->Point2D:
        return Point2D(self.x1, self.cy)
    def _getCb(self)->Point2D:
        return Point2D(self.cx, self.y0)
    def _getCt(self)->Point2D:
        return Point2D(self.cx, self.y1)
    #dtype properties
    x0 = property(_getX0, None, None, 'The left-most x value of the rectangle.') 
    y0 = property(_getY0, None, None, 'The bottom-most y value of the rectangle.')
    x1 = property(_getX1, None, None, 'The right-most x value of the rectangle.')
    y1 = property(_getY1, None, None, 'The top-most y value of the rectangle.') 
    xm = property(_getCenterX, None, None, 'The center x-axis of the rectangle.')
    ym = property(_getCenterY, None, None, 'The center y-axis of the rectangle.')
    w = property(_getW, None, None, 'The width of the rectangle.')
    h = property(_getH, None, None, 'The height of the rectangle')
    #Point2D properties 
    bl = property(_getBl, None, None, 'The bottom left point (x0,y0) of the rectangle.')
    br = property(_getBr, None, None, 'The bottom right point (x1,y0) of the rectangle.')
    tl = property(_getTl, None, None, 'The top left point (x0,y1) of the rectangle.')
    tr = property(_getTr, None, None, 'The top right point (x1,y1) of the rectangle.')
    ml = property(_getCl, None, None, '')
    mr = property(_getCr, None, None, '')
    mt = property(_getCt, None, None, '')
    mb = property(_getCb, None, None, '')
    mm = property(_getCenter, None, None, '')

if __name__=='__main__':
    r = Rect(0,0,2,4)
    data = r.getData()
    print(r)
    print(f'data: \n {r.getData()}')
    print(f'd00, x0: {data[0,0]}, {r.x0}')
    print(f'd01, x1: {data[0,1]}, {r.x1}')
    print(f'd10, y0: {data[1,0]}, {r.y0}')
    print(f'd11, y1: {data[1,1]}, {r.y1}')
    print(f'w, h: {r.w}, {r.h}')
