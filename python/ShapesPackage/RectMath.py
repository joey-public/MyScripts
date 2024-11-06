import numpy as np

from Point2D import Point2D
from Rect import Rect

def rect_crosses_x(r:Rect, x)->bool:
    return x >= r.x0 and x <= r.x1 

def rect_crosses_y(r:Rect, y)->bool:
    return y >= r.y0 and y <= r.y1

def rect_within_y_bounds(r:Rect, y0, y1)->bool:
    return r.y0>=y0 and r.y1<=y1

def rect_within_x_bounds(r:Rect, x0, x1)->bool:
    return r.x0>=x0 and r.x1<=x1


def rect_contains_point(r:Rect, p:Point2D)->bool:
    return rect_crosses_x(r, p.x) and rect_crosses_y(r, p.y)

#checks if r1 is inside r0
def rect_contains_rect(r0:Rect, r1:Rect)->bool:
    return rect_contains_point(r0, r1.bl) and rect_contains_point(r0, r1.tr)

#does r0 pass horizontally all the way through r1
def rect_pass_through_rect_x(r0:Rect, r1:Rect)->bool:
    return rect_within_y_bounds(r0, r1.y0, r1.y1) and rect_crosses_x(r0, r1.x0) and rect_crosses_x(r0, r1.x1)

#does r0 pass vertially all the way through r1
def rect_pass_through_rect_y(r0:Rect, r1:Rect)->bool:
    return rect_within_x_bounds(r0, r1.x0, r1.x1) and rect_crosses_y(r0, r1.y0) and rect_crosses_y(r0, r1.y1)

def rect_pass_into_rect_left(r0:Rect, r1:Rect)->bool:
    return rect_within_y_bounds(r0, r1.y0, r1.y1) and rect_crosses_x(r0, r1.x0) and not(rect_crosses_x(r0, r1.x1))

def rect_pass_into_rect_right(r0:Rect, r1:Rect)->bool:
    return rect_within_y_bounds(r0, r1.y0, r1.y1) and not(rect_crosses_x(r0, r1.x0)) and rect_crosses_x(r0, r1.x1)

def rect_pass_into_rect_bottom(r0:Rect, r1:Rect)->bool:
    return rect_within_x_bounds(r0, r1.x0,r1.x1) and rect_crosses_y(r0, r1.y0) and not(rect_crosses_y(r0, r1.y1))

def rect_pass_into_rect_top(r0:Rect, r1:Rect)->bool:
    return rect_within_x_bounds(r0, r1.x0,r1.x1) and not(rect_crosses_y(r0, r1.y0)) and rect_crosses_y(r0, r1.y1) 

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
