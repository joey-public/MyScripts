import random
import unittest

import numpy as np

from Shape import _Shape
from Point2D import Point2D
from Rect import Rect

#class Shape(unittest.TestCase):
#    def test_xform(self):
#        pass
#    def test_translate(self):
#        pass
#    def test_moveTo(self):
#        pass
#    def test_stretch(self):
#        pass
#    def test_rot90(self):
#        pass

#TODO: implememnt metaprogramming @rand_test 
class TestPoint2D(unittest.TestCase):
    #methods inhereted and overwritten from base _Shape class
    # test these once in the TestShape class
    # methods implemented by Point2D
    def test__eq__(self):
        self.assertEqual(Point2D(3,4), Point2D(3,4))
        self.assertEqual(Point2D(0,0), Point2D(0,0))
        self.assertEqual(Point2D(-3,-4), Point2D(-3,-4))
        self.assertEqual(Point2D(3,-4), Point2D(3,-4))
        self.assertNotEqual(Point2D(7,2), Point2D(2,7))
        self.assertNotEqual(Point2D(3,4), Point2D(3,-4))
#    def test__hash__(self):
#        self.assertTrue(True)
    def test_getData(self):
        #test simple point with no dtype passed
        data = Point2D(3,4).getData()
        #expedt to default the type to float
        expected_data = np.array([[3],[4]], np.float64)
        self.assertEqual(type(data), type(expected_data))
        self.assertEqual(data.dtype, expected_data.dtype)
        self.assertEqual(data.shape, expected_data.shape)
        self.assertEqual(data[0,0], expected_data[0,0])
        self.assertEqual(data[1,0], expected_data[1,0])
        #test several random points with int and float dtypes 
        ntests = 10
        dtypes = [np.int64, np.float64]
        for i in range(ntests):
            for dt in dtypes:
                x = random.randint(-100,100)
                y = random.randint(-100,100)
                data = Point2D(x, y, dt).getData()
                expected_data = np.array([[x], [y]], dt)
                self.assertEqual(type(data), type(expected_data))
                self.assertEqual(data.dtype, expected_data.dtype)
                self.assertEqual(data.shape, expected_data.shape)
                self.assertEqual(data[0,0], expected_data[0,0])
                self.assertEqual(data[1,0], expected_data[1,0])
    def test_updateData(self):
        p = Point2D(3,7)
        new_data = np.array([[2], [4]])
        p.updateData(new_data)
        expected_p = Point2D(2,4)
        self.assertEqual(p, expected_p)
        ntests = 10
        dtypes = [np.int64, np.float64]
        for i in range(ntests):
            for dt in dtypes:
                x = random.randint(-100,100)
                y = random.randint(-100,100)
                p = Point2D(x,y)
                x = random.randint(-100,100)
                y = random.randint(-100,100)
                new_data = np.array([[x], [y]])
                p.updateData(new_data)
                expected_p = Point2D(x,y)
                self.assertEqual(p, expected_p)
    def test_getPos(self):
        pos = Point2D(9.7, 7.9).getPos()
        expected_pos = np.array([[9.7], [7.9]])
        self.assertEqual(type(pos), type(expected_pos))
        self.assertEqual(pos.dtype, expected_pos.dtype)
        self.assertEqual(pos.shape, expected_pos.shape)
        self.assertEqual(pos[0,0], expected_pos[0,0])
        self.assertEqual(pos[1,0], expected_pos[1,0])
    def test_x(self):
        x = Point2D(9,7).x
        expected_x = 9
        self.assertEqual(x, expected_x)
    def test_y(self):
        y = Point2D(18274,8726).y
        expected_y = 8726
        self.assertEqual(y, expected_y)

class TestRect(unittest.TestCase):
    def test__eq__(self):
        ntests = 10
        for i in range(ntests):
            x0 = random.randint(-100,100)
            y0 = random.randint(-100,100)
            w = random.randint(-100,100)
            h = random.randint(-100,100)
            self.assertEqual(Rect(x0,y0,w,h), Rect(x0,y0,w,h))
        self.assertNotEqual(Rect(0,0,10,10), Rect(0,0,1,1))
#    def test__hash__(self):
#        pass
    def test_getData(self):
        ntests = 10
        dtypes = [np.int64, np.float64]
        for i in range(ntests):
            for dt in dtypes:
                x = random.randint(-100,100)
                y = random.randint(-100,100)
                w = random.randint(-100,100)
                h = random.randint(-100,100)
                r = Rect(x,y,w,h,dt)
                data = r.getData()
                expected_data = np.array([[r.x0, r.x1], 
                                          [r.y0, r.y1]], dt)
                self.assertEqual(type(data), type(expected_data))
                self.assertEqual(data.dtype, expected_data.dtype)
                self.assertEqual(data.shape, expected_data.shape)
                self.assertEqual(data[0,0], expected_data[0,0])
                self.assertEqual(data[1,0], expected_data[1,0])
    def test_updateData(self):
        ntests = 100
        dtypes = [np.int64, np.float64]
        for i in range(ntests):
            for dt in dtypes:
                x = random.randint(-100,100)
                y = random.randint(-100,100)
                w = random.randint(-100,100)
                h = random.randint(-100,100)
                r = Rect(x,y,w,h,dt)
                x = random.randint(-100,100)
                y = random.randint(-100,100)
                w  = random.randint(-100,100)
                h  = random.randint(-100,100)
                data = np.array([[x, x+w], 
                                 [y, y+h]], dtype=dt)
                r.updateData(data)
                x0 = min(data[0,0], data[0,1])
                x1 = max(data[0,0], data[0,1])
                y0 = min(data[1,0], data[1,1])
                y1 = max(data[1,0], data[1,1])
                expected_r = Rect(x0, y0, x1-x0, y1-y0)
                self.assertEqual(r, expected_r)
    def test_getPos(self):
        pos = Rect(9.7, 7.9, 10.3, 39.6).getPos()
        expected_pos = np.array([[9.7], [7.9]])
        self.assertEqual(type(pos), type(expected_pos))
        self.assertEqual(pos.dtype, expected_pos.dtype)
        self.assertEqual(pos.shape, expected_pos.shape)
        self.assertEqual(pos[0,0], expected_pos[0,0])
        self.assertEqual(pos[1,0], expected_pos[1,0])
#    def test__getMinX(self):
#        pass
#    def test__getMaxX(self):
#        pass
#    def test__getMinY(self):
#        pass
#    def test__getMaxY(self):
#        pass
    def test_properties(self):
        ntests = 100
        dtypes = [np.int64, np.float64]
        for i in range(ntests):
            for dt in dtypes:
                x = random.randint(-100,100)
                y = random.randint(-100,100)
                w = random.randint(-100,100)
                h = random.randint(-100,100)
                r0 = Rect(x,y,w,h,dt)
                r1 = Rect(x,y,w,h,dt)

                self.assertEqual(r0.x0, r1.x0)
                self.assertEqual(r0.y0, r1.y0)
                self.assertEqual(r0.x1, r1.x1)
                self.assertEqual(r0.y1, r1.y1)
                self.assertEqual(r0.xm, r1.xm)
                self.assertEqual(r0.ym, r1.ym)
                self.assertEqual(r0.w, r1.w)
                self.assertEqual(r0.h, r1.h)

                self.assertEqual(r0.bl, r1.bl)
                self.assertEqual(r0.br, r1.br)
                self.assertEqual(r0.tl, r1.tl)
                self.assertEqual(r0.tr, r1.tr)

                self.assertEqual(r0.ml, r1.ml)
                self.assertEqual(r0.mr, r1.mr)
                self.assertEqual(r0.mt, r1.mt)
                self.assertEqual(r0.mb, r1.mb)
                
                self.assertEqual(r0.mm, r1.mm)

if __name__=='__main__':
    unittest.main()

