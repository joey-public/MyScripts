import numpy as np

from .Point2D import Point2D
from .Rect import Rect
from .RectArray import RectArray

def rect_crosses_x(r:Rect, x)->bool:
    return x >= r.x0 and x <= r.x1 

def rect_crosses_y(r:Rect, y)->bool:
    return y >= r.y0 and y <= r.y1

#is r0 COMPLETELY within y0 and y1
def rect_within_y_bounds(r:Rect, y0, y1)->bool:
    return r.y0>=y0 and r.y1<=y1

#is r0 COMPLETELY within x0 and x1
def rect_within_x_bounds(r:Rect, x0, x1)->bool:
    return r.x0>=x0 and r.x1<=x1

#checks is r contains p
def rect_contains_point(r:Rect, p:Point2D)->bool:
    return rect_crosses_x(r, p.x) and rect_crosses_y(r, p.y)

#checks if r0 contains r1
def rect_contains_rect(r0:Rect, r1:Rect)->bool:
    return rect_contains_point(r0, r1.bl) and rect_contains_point(r0, r1.tr)

#does r0 pass horizontally all the way through r1
def rect_pass_through_rect_x(r0:Rect, r1:Rect)->bool:
    return rect_within_y_bounds(r0, r1.y0, r1.y1) and rect_crosses_x(r0, r1.x0) and rect_crosses_x(r0, r1.x1)

#does r0 pass vertially all the way through r1
def rect_pass_through_rect_y(r0:Rect, r1:Rect)->bool:
    return rect_within_x_bounds(r0, r1.x0, r1.x1) and rect_crosses_y(r0, r1.y0) and rect_crosses_y(r0, r1.y1)

#does r0 pass horizontally into r1 from the left
def rect_pass_into_rect_left(r0:Rect, r1:Rect)->bool:
    return rect_within_y_bounds(r0, r1.y0, r1.y1) and rect_crosses_x(r0, r1.x0) and not(rect_crosses_x(r0, r1.x1))

#does r0 pass horizontally into r1 from the right 
def rect_pass_into_rect_right(r0:Rect, r1:Rect)->bool:
    return rect_within_y_bounds(r0, r1.y0, r1.y1) and not(rect_crosses_x(r0, r1.x0)) and rect_crosses_x(r0, r1.x1)

#does r0 pass vertically into r1 from the bottom 
def rect_pass_into_rect_bottom(r0:Rect, r1:Rect)->bool:
    return rect_within_x_bounds(r0, r1.x0,r1.x1) and rect_crosses_y(r0, r1.y0) and not(rect_crosses_y(r0, r1.y1))

#does r0 pass vertically into r1 from the top
def rect_pass_into_rect_top(r0:Rect, r1:Rect)->bool:
    return rect_within_x_bounds(r0, r1.x0,r1.x1) and not(rect_crosses_y(r0, r1.y0)) and rect_crosses_y(r0, r1.y1) 

#does r0 overlap with r1
def rect_overlaps_rect(r0:Rect, r1:Rect)->bool:
    if rect_pass_through_rect_x(r0, r1): 
        return True
    if rect_pass_through_rect_y(r0, r1): 
        return True
    if rect_pass_into_rect_left(r0, r1): 
        return True
    if rect_pass_into_rect_right(r0, r1):
        return True
    if rect_pass_into_rect_top(r0, r1):
        return True
    if rect_pass_into_rect_bottom(r0, r1):
        return True
    return False

def get_overlap_rect(r0:Rect, r1:Rect)->Rect:
    if rect_pass_through_rect_x(r0, r1): 
        return Rect(r1.x0, r0.y0, r1.w, r0.h) 
    if rect_pass_through_rect_y(r0, r1): 
        return Rect(r0.x0, r1.y0, r0.w, r1.h)
    if rect_pass_into_rect_left(r0, r1): 
        x0 = r1.x0
        y0 = r0.y0
        w = r1.w - (r1.x1-r0.x1)
        h = r0.h
        return Rect(x0,y0,w,h)
    if rect_pass_into_rect_right(r0, r1):
        x0 = r0.x0
        y0 = r0.y0
        w = (r1.x1-r0.x0)
        h = r0.h
        return Rect(x0,y0,w,h)
    if rect_pass_into_rect_top(r0, r1):
        x0 = r0.x0
        y0 = r0.y0
        w = r0.w
        h = (r1.y1-r0.y0)
        return Rect(x0,y0,w,h)
    if rect_pass_into_rect_bottom(r0, r1):
        x0 = r0.x0
        y0 = r1.y0
        w = r0.w
        h = (r0.y1-r1.y0)
        return Rect(x0,y0,w,h)
    return Rect(0,0,0,0) 
    
def get_overlap_rect_array_h(r0:Rect, r1:Rect, r2:Rect, pitch, enc)->RectArray:
    if not(rect_overlaps_rect(r0, r1)): return None
    r_olap = get_overlap_rect(r0, r1)
    if not(r2.w*r2.h < r_olap.w*r_olap.h): return None
    ncols = 1
    h_rects = RectArray(r2, pitch, 0, 1, ncols)
    while h_rects.bbox.w <= r_olap.w-2*enc:
        h_rects.ncols = h_rects.ncols + 1
    h_rects.moveTo(0,0)
    x = r_olap.xm - h_rects.bbox.w/2
    y = r_olap.ym - h_rects.bbox.h/2
    h_rects.moveTo(x,y)
    return h_rects

def get_overlap_rect_array_v(r0:Rect, r1:Rect, r2:Rect, pitch, enc)->RectArray:
    if not(rect_overlaps_rect(r0, r1)): return None
    r_olap = get_overlap_rect(r0, r1)
    if not(r2.w*r2.h < r_olap.w*r_olap.h): return None
    nrows = 1
    v_rects = RectArray(r2, 0, pitch, nrows, 1)
    while v_rects.bbox.h <= r_olap.h-2*enc:
        v_rects.nrows = v_rects.nrows + 1
    v_rects.moveTo(0,0)
    x = r_olap.xm - v_rects.bbox.w/2
    y = r_olap.ym - v_rects.bbox.h/2
    v_rects.moveTo(x,y)
    return v_rects

def get_overlap_rect_array(r0:Rect, r1:Rect, r2:Rect, pitch:Point2D, enc:float)->RectArray:
    if not(rect_overlaps_rect(r0, r1)): return None
    r_olap = get_overlap_rect(r0, r1)
    if not(r2.w*r2.h < r_olap.w*r_olap.h): return None
    rects = RectArray(r2, pitch.x, pitch.y, 1, 1)
    while rects.bbox.w <= r_olap.w-2*enc:
        rects.ncols = rects.ncols + 1
    while rects.bbox.h <= r_olap.h-2*enc:
        rects.nrows = rects.nrows + 1
    rects.moveTo(0,0)
    x = r_olap.xm - rects.bbox.w/2
    y = r_olap.ym - rects.bbox.h/2
    rects.moveTo(x,y)
    return rects

