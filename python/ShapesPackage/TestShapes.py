import random
import unittest

import numpy as np

from Shape import _Shape
from Point2D import Point2D
from Rect import Rect
from RectArray import RectArray
from RectGrid import RectGrid
import RectMath as rm

NTRIALS = 100
MIN_VAL = -1000
MAX_VAL = 1000

class Shape(unittest.TestCase):
    test_dict_0 = {
            (10,4) : Point2D(10,14), 
            (0, 0) : Point2D(1,1),
            (0, 0) : Point2D(0,0),
            (1.7, 10.2) : Point2D(1.7,0),
            (-1, 10.2) : Point2D(12,0),
            (-1, 10.2) : Point2D(12.7,12),
            (-11.4, 10.2) : Point2D(3.8, 129.3),
            (101.478, -123810.452) : Point2D(347, 1083.897),
            (0,0): Rect(0,0,10,10),
            (12.4, 34.7): Rect(-10,10,4,2.7),
            (123.789, 12347.809): Rect(99.65, 87.90, 12.659, 11.75),
            (124, 10): RectArray(Rect(0,0,10,10), 12, 12, 4, 2),
            (12, -12): RectArray(Rect(10.4,0.10,10,10), 12.7, 2, 400, 20), 
            (124.8972, 0.220): RectArray(Rect(0,0,10,10), 12, 12, 4, 2), 
            (-124.8972, -0.020): RectArray(Rect(0,0,10,10), 12, 12, 4, 2), 
    }
    def test_translate(self):
        test_dict = self.test_dict_0
        for key in test_dict.keys():
            s = test_dict[key]
            dx, dy = key
            if type(s) == Point2D:
                exp_s = Point2D(s.x+dx, s.y+dy)
            if type(s) == Rect:
                exp_s = Rect(s.x0+dx, s.y0+dy, s.w, s.h)
            if type(s) == RectArray:
                r = Rect(s.r0.x0+dx, s.r0.y0+dy, s.r0.w, s.r0.h)
                exp_s = RectArray(r, s.pitch.x, s.pitch.y, s.nrows, s.ncols)
            s.translate(dx, dy)
            m = f'\ns: {type(s)}\n{s.getPos()}\n---\nexp_s: {type(s)}\n{exp_s.getPos()}' 
            self.assertEqual(s, exp_s, msg=m)
    def test_moveTo(self):
        test_dict = self.test_dict_0
        for key in test_dict.keys():
            s = test_dict[key]
            xpos, ypos = key
            if type(s) == Point2D:
                exp_s = Point2D(xpos, ypos)
            if type(s) == Rect:
                exp_s = Rect(xpos, ypos, s.w, s.h)
            if type(s) == RectArray:
                r = Rect(xpos, ypos, s.r0.w, s.r0.h)
                exp_s = RectArray(r, s.pitch.x, s.pitch.y, s.nrows, s.ncols)
            s.moveTo(xpos, ypos)
            m = f'\ns: {type(s)}\n{s.getPos()}\n---\nexp_s: {type(s)}\n{exp_s.getPos()}' 
            self.assertEqual(s, exp_s, msg=m)
    def test_scale(self):
        test_dict = self.test_dict_0
        for key in test_dict.keys():
            s = test_dict[key]
            sf0, sf1 = key
            sf = abs(1/(sf0+sf1+0.1))
            if type(s) == Point2D:
                exp_s = Point2D(sf*s.x, sf*s.y)
            if type(s) == Rect:
                exp_s = Rect(sf*s.x0, sf*s.y0, sf*s.w, sf*s.h)
            if type(s) == RectArray:
                r = Rect(sf*s.r0.x0, sf*s.r0.y0, sf*s.r0.w, sf*s.r0.h)
                exp_s = RectArray(r, sf*s.pitch.x, sf*s.pitch.y, s.nrows, s.ncols)
            s.scale(sf)
            m = f'\ns: {type(s)}\n{s.getPos()}\n---\nexp_s: {type(s)}\n{exp_s.getPos()}' 
            self.assertEqual(s, exp_s, msg=m)
    def test_stretch(self):
        test_dict = self.test_dict_0
        for key in test_dict:
            s = test_dict[key]
            sx, sy = (abs(key[0]), abs(key[1]))
            if type(s) == Point2D:
                exp_s = Point2D(s.x, s.y)
            if type(s) == Rect:
                exp_s = Rect(s.x0, s.y0, sx*s.w, sy*s.h)
            if type(s) == RectArray:
                r = Rect(s.r0.x0, s.r0.y0, sx*s.r0.w, sy*s.r0.h)
                exp_s = RectArray(r, s.pitch.x, s.pitch.y, s.nrows, s.ncols)
            s.stretch(sx, sy)
            m = f'\ns: {type(s)}\n{s.getPos()}\n---key: {key}\nexp_s: {type(s)}\n{exp_s.getPos()}' 
            self.assertEqual(s, exp_s, msg=m)
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
        dtypes = [np.int64, np.float64]
        for i in range(NTRIALS):
            for dt in dtypes:
                x = random.randint(MIN_VAL,MAX_VAL)
                y = random.randint(MIN_VAL,MAX_VAL)
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
        dtypes = [np.int64, np.float64]
        for i in range(NTRIALS):
            for dt in dtypes:
                x = random.randint(MIN_VAL,MAX_VAL)
                y = random.randint(MIN_VAL,MAX_VAL)
                p = Point2D(x,y)
                x = random.randint(MIN_VAL,MAX_VAL)
                y = random.randint(MIN_VAL,MAX_VAL)
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
        for i in range(NTRIALS):
            x0 = random.randint(MIN_VAL,MAX_VAL)
            y0 = random.randint(MIN_VAL,MAX_VAL)
            w = random.randint(MIN_VAL,MAX_VAL)
            h = random.randint(MIN_VAL,MAX_VAL)
            self.assertEqual(Rect(x0,y0,w,h), Rect(x0,y0,w,h))
        self.assertNotEqual(Rect(0,0,10,10), Rect(0,0,1,1))
#    def test__hash__(self):
#        pass
    def test_getData(self):
        dtypes = [np.int64, np.float64]
        for i in range(NTRIALS):
            for dt in dtypes:
                x = random.randint(MIN_VAL,MAX_VAL)
                y = random.randint(MIN_VAL,MAX_VAL)
                w = random.randint(MIN_VAL,MAX_VAL)
                h = random.randint(MIN_VAL,MAX_VAL)
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
        dtypes = [np.int64, np.float64]
        for i in range(NTRIALS):
            for dt in dtypes:
                x = random.randint(MIN_VAL,MAX_VAL)
                y = random.randint(MIN_VAL,MAX_VAL)
                w = random.randint(MIN_VAL,MAX_VAL)
                h = random.randint(MIN_VAL,MAX_VAL)
                r = Rect(x,y,w,h,dt)
                x = random.randint(MIN_VAL,MAX_VAL)
                y = random.randint(MIN_VAL,MAX_VAL)
                w  = random.randint(MIN_VAL,MAX_VAL)
                h  = random.randint(MIN_VAL,MAX_VAL)
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
        dtypes = [np.int64, np.float64]
        for i in range(NTRIALS):
            for dt in dtypes:
                x = random.randint(MIN_VAL,MAX_VAL)
                y = random.randint(MIN_VAL,MAX_VAL)
                w = random.randint(MIN_VAL,MAX_VAL)
                h = random.randint(MIN_VAL,MAX_VAL)
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

class TestRectArray(unittest.TestCase):
    def test__eq__(self):
        for i in range(NTRIALS):
            x = random.randint(MIN_VAL,MAX_VAL)
            y = random.randint(MIN_VAL,MAX_VAL)
            w = random.randint(MIN_VAL,MAX_VAL)
            h = random.randint(MIN_VAL,MAX_VAL)
            xp = random.randint(0,MAX_VAL)
            yp = random.randint(0,MAX_VAL)
            nr = random.randint(1,MAX_VAL)
            nc = random.randint(1,MAX_VAL)
            ra0 =  RectArray(Rect(x,y,w,h), xp, yp, nr, nc)
            ra1 = RectArray(Rect(x,y,w,h), xp, yp, nr, nc)
            self.assertEqual(ra0, ra1)
    def test_getData(self):
        for i in range(NTRIALS):
            x = random.randint(MIN_VAL,MAX_VAL)
            y = random.randint(MIN_VAL,MAX_VAL)
            w = random.randint(MIN_VAL,MAX_VAL)
            h = random.randint(MIN_VAL,MAX_VAL)
            xp = random.randint(0,MAX_VAL)
            yp = random.randint(0,MAX_VAL)
            nr = random.randint(1,MAX_VAL)
            nc = random.randint(1,MAX_VAL)
            data =  RectArray(Rect(x,y,w,h), xp, yp, nr, nc).getData()
            expected_data = Rect(x,y,w,h).getData()
            self.assertEqual(type(data), type(expected_data))
            self.assertEqual(data.dtype, expected_data.dtype)
            self.assertEqual(data.shape, expected_data.shape)
            self.assertEqual(data[0,0], expected_data[0,0])
            self.assertEqual(data[1,0], expected_data[1,0])
    def test_updateData(self):
        for i in range(NTRIALS):
            x = random.randint(MIN_VAL,MAX_VAL)
            y = random.randint(MIN_VAL,MAX_VAL)
            w = random.randint(MIN_VAL,MAX_VAL)
            h = random.randint(MIN_VAL,MAX_VAL)
            xp = random.randint(0,MAX_VAL)
            yp = random.randint(0,MAX_VAL)
            nr = random.randint(1,MAX_VAL)
            nc = random.randint(1,MAX_VAL)
            ra =  RectArray(Rect(x,y,w,h), xp, yp, nr, nc)

            x = random.randint(MIN_VAL,MAX_VAL)
            y = random.randint(MIN_VAL,MAX_VAL)
            w = random.randint(MIN_VAL,MAX_VAL)
            h = random.randint(MIN_VAL,MAX_VAL)
            xp = random.randint(0,MAX_VAL)
            yp = random.randint(0,MAX_VAL)
            nr = random.randint(1,MAX_VAL)
            nc = random.randint(1,MAX_VAL)
            new_data =  Rect(x,y,w,h).getData()
            ra.updateData(new_data)
            self.assertEqual(ra.r0, Rect(x,y,w,h))
    def test_getPos(self):
        r0 = Rect(9.7, 7.9, 10.3, 39.6)
        pos = RectArray(r0,12,10,19,134).getPos()
        expected_pos = np.array([[9.7], [7.9]])
        self.assertEqual(type(pos), type(expected_pos))
        self.assertEqual(pos.dtype, expected_pos.dtype)
        self.assertEqual(pos.shape, expected_pos.shape)
        self.assertEqual(pos[0,0], expected_pos[0,0])
        self.assertEqual(pos[1,0], expected_pos[1,0])
    def test_propertes(self):
        for i in range(NTRIALS):
            x = random.randint(MIN_VAL,MAX_VAL)
            y = random.randint(MIN_VAL,MAX_VAL)
            w = random.randint(MIN_VAL,MAX_VAL)
            h = random.randint(MIN_VAL,MAX_VAL)
            xp = random.randint(0,MAX_VAL)
            yp = random.randint(0,MAX_VAL)
            nr = random.randint(1,MAX_VAL)
            nc = random.randint(1,MAX_VAL)
            ra0 = RectArray(Rect(x,y,w,h), xp, yp, nr, nc)
            ra1 = RectArray(Rect(x,y,w,h), xp, yp, nr, nc)
            self.assertEqual(ra0.r0, ra1.r0)
            self.assertEqual(ra0.pitch, ra1.pitch)
            self.assertEqual(ra0.dx, ra1.dx)
            self.assertEqual(ra0.dy, ra1.dy)
            self.assertEqual(ra0.bbox, ra1.bbox)

class TestRectGrid(unittest.TestCase):
    def test__eq__(self):
        for i in range(NTRIALS):
            x = random.randint(MIN_VAL,MAX_VAL)
            y = random.randint(MIN_VAL,MAX_VAL)
            w = random.randint(MIN_VAL,MAX_VAL)
            h = random.randint(MIN_VAL,MAX_VAL)
            xp = random.randint(0,MAX_VAL)
            yp = random.randint(0,MAX_VAL)
            nr = random.randint(1,MAX_VAL)
            nc = random.randint(1,MAX_VAL)
            hra = RectArray(Rect(x,y,w,h), 0, yp, nr, 1)
            vra = RectArray(Rect(x,y,w,h), xp, 0, 1, nc)
            rg0 = RectGrid(hra, vra)
            rg1 = RectGrid(hra, vra)
            self.assertEqual(rg0, rg1)
    def test_getData(self):
        for i in range(NTRIALS):
            x = random.randint(MIN_VAL,MAX_VAL)
            y = random.randint(MIN_VAL,MAX_VAL)
            w = random.randint(MIN_VAL,MAX_VAL)
            h = random.randint(MIN_VAL,MAX_VAL)
            xp = random.randint(0,MAX_VAL)
            yp = random.randint(0,MAX_VAL)
            nr = random.randint(1,MAX_VAL)
            nc = random.randint(1,MAX_VAL)
            hra = RectArray(Rect(x,y,w,h), 0, yp, nr, 1)
            vra = RectArray(Rect(x,y,w,h), xp, 0, 1, nc)
            rg0 = RectGrid(hra, vra)
            data = RectGrid(hra, vra).getData()
            expected_data = np.array([ [hra.r0.x0, hra.r0.x1, vra.r0.x0, vra.r0.x1], 
                                       [hra.r0.y0, hra.r0.y1, vra.r0.y0, vra.r0.y1] ])
            self.assertEqual(type(data), type(expected_data))
            self.assertEqual(data.dtype, expected_data.dtype)
            self.assertEqual(data.shape, expected_data.shape)
            self.assertEqual(data[0,0], expected_data[0,0])
            self.assertEqual(data[1,0], expected_data[1,0])
#    def test_getPos(self):
#        pass
#    def test_updateData(self):
#        pass 
#    def test_properties(self):
#        pass

class TestRectMath(unittest.TestCase):
    def test_rect_crosses_x(self):
        x = 0
        r = Rect(0,0,10,10)
        m = f'\nx: {x}, Rect x0, x1: {r.x0}, {r.x1}\n'
        self.assertEqual(rm.rect_crosses_x(r, x), True, msg=m)
        x = -1
        self.assertEqual(rm.rect_crosses_x(r, x), False, msg=m)
        r = Rect(-10,10,-20,10)
        self.assertEqual(rm.rect_crosses_x(r, x), False, msg=m)
        r = Rect(-10,10,20,10)
        self.assertEqual(rm.rect_crosses_x(r, x), True, msg=m)
        x = 1.345
        r = Rect(0,0,1.344,100)
        self.assertEqual(rm.rect_crosses_x(r, x), False, msg=m)
        r = Rect(0,0,1.346,100)
        self.assertEqual(rm.rect_crosses_x(r, x), True, msg=m)
    def test_rect_crosses_y(self):
        y = 0
        r = Rect(0,0,10,10)
        m = f'\ny: {y}, Rect y0, y1: {r.y0}, {r.y1}\n'
        self.assertEqual(rm.rect_crosses_y(r, y), True, msg=m)
        y = 10
        self.assertEqual(rm.rect_crosses_y(r, y), True, msg=m)
        y = 1
        self.assertEqual(rm.rect_crosses_y(r, y), True, msg=m)
        y = -1
        self.assertEqual(rm.rect_crosses_y(r, y), False, msg=m)
        r = Rect(0,0.12330,10,1092.8)
        y = 1092.9
        self.assertEqual(rm.rect_crosses_y(r, y), True, msg=m)
        y = 1093.9
        self.assertEqual(rm.rect_crosses_y(r, y), False, msg=m)
    def test_rect_within_x_bounds(self):
        xmin = 0
        xmax = 10
        r = Rect(0,0,10,10)
        self.assertEqual(rm.rect_within_x_bounds(r, xmin, xmax), True,
                                                                 msg=f'\nxmin, xmax: {xmin}, {xmax}\nr.x0, r.x1: {r.x0}, {r.x1}\n')
        xmin, xmax = (-10,1) 
        self.assertEqual(rm.rect_within_x_bounds(r, xmin, xmax), False, 
                                                                 msg=f'\nxmin, xmax: {xmin}, {xmax}\nr.x0, r.x1: {r.x0}, {r.x1}\n')
        xmin, xmax = (-10,-1) 
        self.assertEqual(rm.rect_within_x_bounds(r, xmin, xmax), False, 
                                                                 msg=f'\nxmin, xmax: {xmin}, {xmax}\nr.x0, r.x1: {r.x0}, {r.x1}\n')
        xmin, xmax = (0,10.000001) 
        self.assertEqual(rm.rect_within_x_bounds(r, xmin, xmax), True, 
                                                                 msg=f'\nxmin, xmax: {xmin}, {xmax}\nr.x0, r.x1: {r.x0}, {r.x1}\n')
        xmin, xmax = (0.000001,10.000001) 
        self.assertEqual(rm.rect_within_x_bounds(r, xmin, xmax), False, 
                                                                 msg=f'\nxmin, xmax: {xmin}, {xmax}\nr.x0, r.x1: {r.x0}, {r.x1}\n')
        xmin, xmax = (0,9.9999999) 
        self.assertEqual(rm.rect_within_x_bounds(r, xmin, xmax), False, 
                                                                 msg=f'\nxmin, xmax: {xmin}, {xmax}\nr.x0, r.x1: {r.x0}, {r.x1}\n')
    def test_rect_within_y_bounds(self):
        ymin = 0
        ymax = 10
        r = Rect(0,0,10,10)
        self.assertEqual(rm.rect_within_y_bounds(r, ymin, ymax), True,
                                                                 msg=f'\nymin, ymax: {ymin}, {ymax}\nr.y0, r.y1: {r.y0}, {r.y1}\n')
        r = Rect(0,0,10,10.0001)
        self.assertEqual(rm.rect_within_y_bounds(r, ymin, ymax), False,
                                                                 msg=f'\nymin, ymax: {ymin}, {ymax}\nr.y0, r.y1: {r.y0}, {r.y1}\n')
        r = Rect(0,0.001,10,10)
        self.assertEqual(rm.rect_within_y_bounds(r, ymin, ymax), False,
                                                                 msg=f'\nymin, ymax: {ymin}, {ymax}\nr.y0, r.y1: {r.y0}, {r.y1}\n')
        r = Rect(0,0,10,10)
        ymin, ymax = (0.1, 11)
        self.assertEqual(rm.rect_within_y_bounds(r, ymin, ymax), False,
                                                                 msg=f'\nymin, ymax: {ymin}, {ymax}\nr.y0, r.y1: {r.y0}, {r.y1}\n')
        ymin, ymax = (-0.1, 10.01)
        self.assertEqual(rm.rect_within_y_bounds(r, ymin, ymax), True,
                                                                 msg=f'\nymin, ymax: {ymin}, {ymax}\nr.y0, r.y1: {r.y0}, {r.y1}\n')
    def test_rect_contains_point(self):
        r = Rect(0,0,10,10)
        p = Point2D(5,5)
        self.assertEqual(rm.rect_contains_point(r, p), True)
        p = r.bl
        self.assertEqual(rm.rect_contains_point(r, p), True)
        p = r.br
        self.assertEqual(rm.rect_contains_point(r, p), True)
        p = r.tl
        self.assertEqual(rm.rect_contains_point(r, p), True)
        p = r.tr
        self.assertEqual(rm.rect_contains_point(r, p), True)
        p = r.mr
        self.assertEqual(rm.rect_contains_point(r, p), True)
        p = r.ml
        self.assertEqual(rm.rect_contains_point(r, p), True)
        p = r.mt
        self.assertEqual(rm.rect_contains_point(r, p), True)
        p = r.mb
        self.assertEqual(rm.rect_contains_point(r, p), True)
        p = Point2D(-1,0)
        self.assertEqual(rm.rect_contains_point(r, p), False)
        p = Point2D(0,-1)
        self.assertEqual(rm.rect_contains_point(r, p), False)
        p = Point2D(0,11)
        self.assertEqual(rm.rect_contains_point(r, p), False)
        p = Point2D(11,11)
        self.assertEqual(rm.rect_contains_point(r, p), False)
    def test_rect_contains_rect(self):
        r0 = Rect(0,0,10,10)
        r1 = Rect(0,0,10,10)
        self.assertEqual(rm.rect_contains_rect(r0,r1), True)
        r1 = Rect(0,3,1,1)
        self.assertEqual(rm.rect_contains_rect(r0,r1), True)
        r1 = Rect(-10,0,10,10)
        self.assertEqual(rm.rect_contains_rect(r0,r1), False)
        r1 = Rect(0,-10,10,10)
        self.assertEqual(rm.rect_contains_rect(r0,r1), False)
        r1 = Rect(0,20,10,10)
        self.assertEqual(rm.rect_contains_rect(r0,r1), False)
        r1 = Rect(20,20,10,10)
        self.assertEqual(rm.rect_contains_rect(r0,r1), False)
    def test_rect_pass_through_rect_x(self):
        pass
    def test_rect_pass_through_rect_y(self):
        pass
    def test_rect_pass_into_rect_left(self):
        pass
    def test_rect_pass_into_rect_right(self):
        pass
    def test_rect_pass_into_rect_top(self):
        pass
    def test_rect_pass_into_rect_bottom(self):
        pass
    def test_rect_overlaps_rect(self):
        pass
    def test_get_overlap_rect(self):
        pass
    def test_get_overlap_rect_array_h(self):
        pass
    def test_get_overlap_rect_array_v(self):
        pass
    def test_get_overlap_rect_array(self):
        pass


if __name__=='__main__':
    unittest.main()

