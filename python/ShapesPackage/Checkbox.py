import pygame as pg

import DrawFuncs as drw
from ShapeContainer import ShapeContainer

from Point2D import Point2D
from Rect import Rect


pygame.font.init()
#A static text Label. For now I have no need or way to update the label 
class TextLabel:
    def __init__(self, label:str, pos:Point2D, **kwargs):
        self.label = label
        self.pos = pos
        self.font_type = 'Open Sans'
        self.font_size = 12
        self.font_color = (255,255,255)
        self.aa = True
        if 'font' in kwargs.keys(): 
            self.font_type = kwargs['font']
        if 'font_size' in kwargs.keys(): 
            self.font_size = kwargs['font_size']
        if 'font_color' in kwargs.keys(): 
            self.font_color = kwargs['font_color']
        pg.font.SysFont(self.font_type, self.font_size)
        self._surface = pg.font.render(self.label, self.aa, self.font_color) 
    def __getSurface(self):
        return self._surface
    surface = property(__getSurface, None, None, 'the pygame surface with the label text')

