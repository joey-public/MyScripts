import numpy as np

class Rect():
    def __init__(self, x0:int, y0:int, w:int, h:int):
        if w < 0:
            return np.zeros(shape=(2,2))
        if h < 0:
            return np.zeros(shape=(2,2))
        self.data = np.array([[x0, y0], [x0+w, y0+h]], dtype=int)
    def x0(self)->int:
        return self.data[0,0]
    def y0(self)->int:
        return self.data[0,1]
    def x1(self)->int:
        return self.data[1,0]
    def y1(self)->int:
        return self.data[1,1]
    def w(self)->int:
        return self.data[1,0] - self.data[0,0]
    def h(self)->int:
        return self.data[1,1] - self.data[0,1]
    def center(self)->tuple:
        x = self.x0() + self.w()/2
        y = self.y0() + self.h()/2
    def scale(self, sx:float, sy:float)->None:
        xform = np.array([ [sx, 0],
                           [0,  sy] ])
        self.data = np.dot(self.data, xform.T) 
    def reflect()->None:
        pass
    def rotate()->None:
        pass
    def translate(self, dx, dy)->None:
        self.data[:,0] += dx  #add dx to column 0
        self.data[:,1] += dy  #add dy to column 1

if __name__=='__main__':
    r0 = Rect(0,0,2,5)
    r1 = Rect(1,1,4,2)
    r2 = Rect(2,3,1,1)
    ar = np.array([r0.data, r1.data, r2.data])
    print(ar)
    print(np.shape(ar))

