import numpy as np

class Rect():
    def __init__(self, x0:int, y0:int, w:int, h:int):
        if w < 0:
            return np.zeros(shape=(2,2))
        if h < 0:
            return np.zeros(shape=(2,2))
        self.data = np.array([[x0, x0+w], [y0, y0+h]], dtype=int)
    def x0(self)->int:
        return np.min(self.data[0,0], self.data[0,1])
    def y0(self)->int:
        return np.min(self.data[1,0], self.data[1,1])
    def x1(self)->int:
        return np.max(self.data[0,0], self.data[0,1])
    def y1(self)->int:
        return np.min(self.data[1,0], self.data[1,1])
    def w(self)->int:
        return self.x1()-self.x0()
#        return self.data[1,0] - self.data[0,0]
    def h(self)->int:
        return self.y1()-self.y0()
#        return self.data[1,1] - self.data[0,1]
    def center(self)->tuple:
        x = self.x0() + self.w()/2
        y = self.y0() + self.h()/2
    def apply_xform(self, xform:np.array)->None:
        if not(xform.shape == (2,2)): return 
        self.data = np.matmul(xform, self.data)
    def rot90(self, anchor = (0,0))->None:
        xform = np.array([[0, -1], 
                          [1, 0]])
        if not(anchor==(0,0)):
            dx, dy = anchor
            self.translate(dx, dy)
            self.apply_xform(xform)
            self.translate(dx,dy)
        self.apply_xform(xform) 
    def scale(self, sx:float, sy:float)->None:
        xform = np.array([ [sx, 0],
                           [0,  sy] ])
        self.apply_xform(xform)
    def reflect()->None:
        pass
    def rotate()->None:
        pass
    def translate(self, dx, dy)->None:
        self.data[:,0] += dx  #add dx to column 0
        self.data[:,1] += dy  #add dy to column 1

if __name__=='__main__':
    r0 = Rect(0,0,1,1)
    r1 = Rect(0,0,1,1)
    r1.scale(7,4)
    r2 = Rect(0,0,1,1)
    r2.scale(12,9)
    rarray = np.hstack((r0.data,r1.data,r2.data))
    print(rarray)
    xform = np.array([[0, -1], 
                      [1, 0]])
    print(np.matmul(xform, rarray))

    r0.rot90()
    r1.rot90()
    r2.rot90()
    print(r0.data)
    print(r1.data)
    print(r2.data)
