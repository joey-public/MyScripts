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
    def test__hash__(self):
        self.assertTrue(True)
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

#class TestRect(unittest.TestCase):
#    def test__eq__(self):
#        pass
#    def test__hash__(self):
#        pass
#    def test_getData(self):
#        pass
#    def test_updateData(self):
#        pass
#    def test_getPos(self):
#        pass
#    def test__getMinX(self):
#        pass
#    def test__getMaxX(self):
#        pass
#    def test__getMinY(self):
#        pass
#    def test__getMaxY(self):
#        pass
#    def test_x0(self):
#        pass
#    def test_y0(self):
#        pass
#    def test_x1(self):
#        pass
#    def test_y1(self):
#        pass
#    def test_xm(self):
#        pass
#    def test_ym(self):
#        pass
#    def test_w(self):
#        pass
#    def test_h(self):
#        pass
#    def test_bl(self):
#        pass
#    def test_br(self):
#        pass
#    def test_tl(self):
#        pass
#    def test_tr(self):
#        pass
#    def test_ml(self):
#        pass
#    def test_mr(self):
#        pass
#    def test_mb(self):
#        pass
#    def test_mt(self):
#        pass
#    def test_mm(self):
#        pass

if __name__=='__main__':
    unittest.main()

