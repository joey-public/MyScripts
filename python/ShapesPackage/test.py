import pygame as pg
import numpy as np

from Shape import _Shape
from Point2D import Point2D
from Rect import Rect
from RectArray import RectArray
from RectGrid import RectGrid
from ShapeContainer import ShapeContainer
import RectMath as rm


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


#TODO: Seperate draw fucns into an isolated module
#TODO: implement **kwargs for the drawing functions
def draw_point(surface, p:Point2D, radius:int, color:tuple):
    if p is None: return 
    pg.draw.circle(surface, color, (p.x, p.y), radius)
def draw_line(surface, p0, p1, line_width:int, color:tuple):
    if p0 is None or p1 is None: return 
    pg.draw.line(surface, color, (p0.x, p0.y), (p1.x, p1.y), line_width)
def draw_rect(surface, r:Rect, outline_width:int, outline_color:tuple):
    draw_line(surface, r.bl, r.tl, outline_width, outline_color)
    draw_line(surface, r.tl, r.tr, outline_width, outline_color)
    draw_line(surface, r.tr, r.br, outline_width, outline_color)
    draw_line(surface, r.bl, r.br, outline_width, outline_color)
def draw_rect_fill(surface, r:Rect, outline_width:int, outline_color:tuple, fill_color:tuple):
    if r is None: return 
    pg.draw.rect(surface, fill_color, pg.Rect(r.x0, r.y0, r.w, r.h))
    draw_rect(surface, r, outline_width, outline_color)
def draw_rect_array(surface, ra:RectArray, outline_width:int, outline_color:tuple):
    if ra is None: return 
    rect = Rect(ra.r0.x0, ra.r0.y0, ra.r0.w, ra.r0.h)
    for r in range(ra.nrows):
        for c in range(ra.ncols):
            draw_rect(surface, rect, outline_width, outline_color)
            rect.translate(ra.pitch.x, 0)
        rect.translate(-1*int(ra.ncols*ra.pitch.x), ra.pitch.y)
    draw_point(surface, ra.bbox.bl, 3, outline_color)
def draw_rect_grid(surface, rg:RectGrid, width0, width1, color):
    if rg is None: return 
    draw_rect_array(surface, rg.h_rects, width0, color)
    draw_rect_array(surface, rg.v_rects, width0, color)
    draw_rect_array(surface, rg.o_rects, width1, color)
def draw_shape_container(surface:pg.Surface, c:ShapeContainer, **kwargs):
    for shape in c._shape_list:
        shape_type = type(shape) 
        if shape_type == Point2D:
            draw_point(surface, shape, 3, COLOR_0)
        if shape_type == Rect:
            draw_rect(surface, shape, 1, COLOR_0)
        if shape_type == RectArray:
            draw_rect_array(surface, shape, 1, COLOR_0)
        if shape_type == RectGrid:
            draw_rect_grid(surface, shape, 1, 3, COLOR_0)

if __name__ == '__main__':
    # pygame setup
    pg.init()
    screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pg.time.Clock()
    running = True
    dt = 0

    canvas = pg.Surface((SCREEN_WIDTH,SCREEN_HEIGHT))
    
    bbox = Rect(0,0,200,100)
    r0 = Rect(0,0,30,80)
    v_rects = RectArray(r0, x_pitch=50, ncols=3)
    v_rects.translate(35, 10)
    r0 = Rect(0,0,210,10)
    h_rects = RectArray(r0, y_pitch=15, nrows=11)
    h_rects.translate(0, -5)
    
    dev = ShapeContainer()
    dev.addShape(bbox)
    dev.addShape(v_rects)
    #dev.addShape(h_rects)
    xpos = SCREEN_WIDTH/2 - bbox.w/2
    ypos = SCREEN_HEIGHT/2 - bbox.h/2
    dev.translate(xpos, ypos)
    
    while running:
        #handle input
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
        #Handle input
        keys = pg.key.get_pressed()
        if keys[pg.K_j]:
            dev.translate(0,-10)
        if keys[pg.K_k]:
            dev.translate(0,10)
        if keys[pg.K_h]:
            dev.translate(-10, 0)
        if keys[pg.K_l]:
            dev.translate(10, 0)
        if keys[pg.K_b]:
            dev.scale(2)
        if keys[pg.K_c]:
            dev.scale(1/2)
        
        #render
        canvas.fill(BG_COLOR)
        draw_shape_container(canvas, dev)

        screen.blit(pg.transform.flip(canvas, False, True), (0,0))
#        screen.blit(canvas, (0,0))
        pg.display.flip()
        #handle fsp
        dt = clock.tick(10) / 1000
    pg.quit()
