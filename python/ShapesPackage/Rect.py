import numpy as np
from Point2D import Point2D
from Shape import _Shape

class Rect(_Shape):
    def __init__(self, x0, y0, w, h, 
                 dtype=np.float64, prec=6,**kwargs):
        self._dtype = dtype
        self._precision = prec
        for key, val in kwargs.items():
            if key == 'dtype':
                self._dtype = val
            if key == 'prec':
                self._precision = prec
        data = np.array([[x0, x0+w], 
                         [y0, y0+h]], dtype=self._dtype)
        x0 = self.__getMinX(data)
        y0 = self.__getMinY(data)
        x1 = self.__getMaxX(data)
        y1 = self.__getMaxY(data)
        self._data = np.round(np.array([ [x0, x1], 
                                         [y0, y1] ], 
                                        dtype=self._dtype), 
                                        self._precision)
    def __eq__(self, other):
        if not(type(other)==type(self)): 
            return False
        return (self.x0==other.x0) and (self.y0==other.y0) and (self.x1==other.x1) and (self.y1==other.y1) and (self._dtype==other._dtype) and (self._precision==other._precision)
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
        x0 = self.__getMinX(new_data)
        y0 = self.__getMinY(new_data)
        x1 = self.__getMaxX(new_data)
        y1 = self.__getMaxY(new_data)
        self._data[0,0] = x0
        self._data[1,0] = y0
        self._data[0,1] = x1
        self._data[1,1] = y1
        self._data = np.round(self._data, self._precision)
    def getData(self):
        return self._data
    def getPos(self):
        a = np.array([self.x0, self.y0])
        a.shape = (2,1)
        return a
    #Properties
    def __getX0(self):
        data = self._data[0,0]
        assert data == self.__getMinX(self._data), f'rect data misformatted, x0 is not min x.'
        return data
    def __getX1(self):
        data = self._data[0,1]
        assert data == self.__getMaxX(self._data), f'rect data misformatted, x1 is not max x1.'
        return data
    def __getY0(self):
        data = self._data[1,0]
        assert data == self.__getMinY(self._data), 'rect data misformatted, y0 is not min y.'
        return data
    def __getY1(self):
        data = self._data[1,1]
        assert data == self.__getMaxY(self._data), f'rect data misformatted, y1 is not max y.'
        return data
    def __getW(self):
        return self.x1-self.x0
    def __getH(self):
        return self.y1-self.y0
    def __getBl(self)->Point2D:
        return Point2D(self.x0, self.y0)
    def __getBr(self)->Point2D:
        return Point2D(self.x1, self.y0)
    def __getTl(self)->Point2D:
        return Point2D(self.x0, self.y1)
    def __getTr(self)->Point2D:
        return Point2D(self.x1, self.y1)
    def __getCenterX(self)->int:
        return int(self.x0 + self.w/2)
    def __getCenterY(self)->int:
        return int(self.y0 + self.h/2)
    def __getCenter(self)->Point2D:
        return Point2D(self.xm, self.ym)
    def __getCl(self)->Point2D:
        return Point2D(self.x0, self.ym)
    def __getCr(self)->Point2D:
        return Point2D(self.x1, self.ym)
    def __getCb(self)->Point2D:
        return Point2D(self.xm, self.y0)
    def __getCt(self)->Point2D:
        return Point2D(self.xm, self.y1)
    #dtype properties
    x0 = property(__getX0, None, None, 'The left-most x value of the rectangle.') 
    y0 = property(__getY0, None, None, 'The bottom-most y value of the rectangle.')
    x1 = property(__getX1, None, None, 'The right-most x value of the rectangle.')
    y1 = property(__getY1, None, None, 'The top-most y value of the rectangle.') 
    xm = property(__getCenterX, None, None, 'The center x-axis of the rectangle.')
    ym = property(__getCenterY, None, None, 'The center y-axis of the rectangle.')
    w = property(__getW, None, None, 'The width of the rectangle.')
    h = property(__getH, None, None, 'The height of the rectangle')
    #Point2D properties 
    bl = property(__getBl, None, None, 'The bottom left point (x0,y0) of the rectangle.')
    br = property(__getBr, None, None, 'The bottom right point (x1,y0) of the rectangle.')
    tl = property(__getTl, None, None, 'The top left point (x0,y1) of the rectangle.')
    tr = property(__getTr, None, None, 'The top right point (x1,y1) of the rectangle.')

    ml = property(__getCl, None, None, '')
    mr = property(__getCr, None, None, '')
    mt = property(__getCt, None, None, '')
    mb = property(__getCb, None, None, '')

    mm = property(__getCenter, None, None, '')
