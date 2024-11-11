import pygame as pg
import time 

import DrawFuncs as drw
import RectMath as rm
from ShapeContainer import ShapeContainer

from Point2D import Point2D
from Rect import Rect

#TODO: Fix the update to note use mouse.get_pressed and actually use the event system
class Checkbox:
    def __init__(self, box:Rect, label:str='', checked:bool=False, **kwargs):
        self.box = box
        self.label = label
        self.checked = checked
        self.outline_color = (255,255,255)
        self.outline_width = 3
        self.fill_color = (55,55,55)
        self.x_width = 3
        self.x_color = (255,0,0)
    def update(self):
        mx, my = pg.mouse.get_pos()
        lmp, mmp, rmp = pg.mouse.get_pressed()
        box_checked = lmp and rm.rect_contains_point(self.box, Point2D(mx,my))
        if box_checked:
            self.checked = not(self.checked)
#            time.sleep(0.001)
    def render(self, surface:pg.Surface):
        mx, my = pg.mouse.get_pos()
        mouse_in_box = rm.rect_contains_point(self.box, Point2D(mx, my)) 
        if self.checked and mouse_in_box:
            drw.drawRect(surface, self.box,
                         outline_color = self.outline_color, 
                         outline_width = self.outline_width, 
                         fill_color = self.fill_color, 
                         fill_pattern = 'x', 
                         fill_pattern_width = self.x_width, 
                         fill_pattern_color = self.x_color) 
        elif self.checked:
            drw.drawRect(surface, self.box,
                         outline_color = self.outline_color, 
                         outline_width = self.outline_width, 
                         fill_color = None, 
                         fill_pattern = 'x', 
                         fill_pattern_width = self.x_width, 
                         fill_pattern_color = self.x_color) 
        elif mouse_in_box:
            drw.drawRect(surface, self.box,
                         outline_color = self.outline_color, 
                         outline_width = self.outline_width, 
                         fill_color = self.fill_color, 
                         fill_pattern = None, 
                         fill_pattern_width = self.x_width, 
                         fill_pattern_color = self.x_color) 

        else:
            drw.drawRect(surface, self.box,
                         outline_color = self.outline_color, 
                         outline_width = self.outline_width, 
                         fill_color = None, 
                         fill_pattern = None, 
                         fill_pattern_width = self.x_width, 
                         fill_pattern_color = self.x_color) 
        lbl_pos = Point2D(self.box.x1+self.box.w/8, self.box.y0)
        drw.drawText(surface, self.label, lbl_pos)
        
