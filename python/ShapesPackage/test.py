import pygame as pg
import numpy as np

from Shape import _Shape
from Point2D import Point2D
from Rect import Rect
from RectArray import RectArray
from RectGrid import RectGrid
from ShapeContainer import ShapeContainer
import RectMath as rm
import DrawFuncs as renderer


SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500

BG_COLOR = (0,0,0,255)
COLOR_0 = (255, 255, 255, 55)
COLOR_1 = (150, 150, 150, 255)
COLOR_2 = (100, 100, 100, 255)
COLOR_RED = (255,0,0,0)
COLOR_GREEN = (0,255,0,0)
COLOR_BLUE = (0,0,255,0)

FILL_WH = 10
FILL_PITCH = 15
FILL_ENC = 15

if __name__ == '__main__':
    # pygame setup
    pg.init()
    screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pg.time.Clock()
    running = True
    dt = 0
    canvas = pg.Surface((SCREEN_WIDTH,SCREEN_HEIGHT))
    
    r0 = Rect(0, 50, 50, 50)
    r1 = Rect(0, 150, 50, 50)
    r2 = Rect(0, 250, 50, 50)
    r3 = Rect(0, 350, 50, 50)
    
    ra = RectArray(Rect(0,50,100,50), y_pitch=100, nrows=4)
    ra.translate(100,0)

    ra1 = RectArray(Rect(0,50,100,50), y_pitch=100, nrows=4, 
                                       x_pitch=150, ncols=2)
    ra1.translate(250,0)
    
    while running:
        #handle input
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
        #render
        canvas.fill(BG_COLOR)
        renderer.drawRect(canvas, r0, 
                          outline_color = (255,255,255), 
                          outline_width = 3, 
                          fill_color = (50,50,50), 
                          fill_pattern = 'x', 
                          fill_pattern_width = 1, 
                          fill_pattern_color = (100,100,100)) 
        renderer.drawRect(canvas, r1, 
                          outline_color = (0,255,0), 
                          outline_width = 3, 
                          fill_color = (50,50,50), 
                          fill_pattern = '*', 
                          fill_pattern_width = 3, 
                          fill_pattern_color = (0,255,0)) 
        renderer.drawRect(canvas, r2, 
                          outline_color = (0,255,0), 
                          outline_width = 3, 
                          fill_color = (50,50,50), 
                          fill_pattern = '|') 
        renderer.drawRect(canvas, r3, 
                          outline_color = (0,255,0), 
                          outline_width = 3, 
                          fill_color = (50,50,50), 
                          fill_pattern = '_', 
                          fill_pattern_width = 3, 
                          fill_pattern_color = (0,255,0)) 
        renderer.drawRectArray(canvas, ra, 
                          outline_color = (255,255,255), 
                          outline_width = 3, 
                          fill_color = (50,50,50), 
                          fill_pattern = '*', 
                          fill_pattern_width = 1, 
                          fill_pattern_color = (100,100,100)) 
        renderer.drawRectArray(canvas, ra1, 
                          outline_color = (255,255,255), 
                          outline_width = 1, 
                          fill_color = None, 
                          fill_pattern = 'x', 
                          fill_pattern_width = 1, 
                          fill_pattern_color = (100,0,0)) 
        screen.blit(pg.transform.flip(canvas, False, True), (0,0))
#        screen.blit(canvas, (0,0))
        pg.display.flip()
        #handle fsp
        dt = clock.tick(10) / 1000
    pg.quit()
