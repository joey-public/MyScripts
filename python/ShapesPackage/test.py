import pygame as pg
import numpy as np

from Shape import _Shape
from Point2D import Point2D
from Rect import Rect
from RectArray import RectArray
from RectGrid import RectGrid
import RectMath as rm


def draw_point(surface, p:Point2D, radius:int, color:tuple):
    pg.draw.circle(surface, color, (p.x, p.y), radius)
def draw_line(surface, p0, p1, line_width:int, color:tuple):
    pg.draw.line(surface, color, (p0.x, p0.y), (p1.x, p1.y), line_width)
def draw_rect(surface, r:Rect, outline_width:int, outline_color:tuple):
    draw_line(surface, r.bl, r.tl, outline_width, outline_color)
    draw_line(surface, r.tl, r.tr, outline_width, outline_color)
    draw_line(surface, r.tr, r.br, outline_width, outline_color)
    draw_line(surface, r.bl, r.br, outline_width, outline_color)
def draw_rect_fill(surface, r:Rect, outline_width:int, outline_color:tuple, fill_color:tuple):
    pg.draw.rect(surface, fill_color, pg.Rect(r.x0, r.y0, r.w, r.h))
    draw_rect(surface, r, outline_width, outline_color)

def draw_rect_array(surface, ra:RectArray):
    rect = Rect(ra.r0.x0, ra.r0.y0, ra.r0.w, ra.r0.h)
    for r in range(ra.nrows):
        for c in range(ra.ncols):
            draw_rect(surface, rect, 1, COLOR_0)
            rect.translate(ra.pitch.x, 0)
        rect.translate(-1*int(ra.ncols*ra.pitch.x), ra.pitch.y)
    draw_point(ra.bbox.bl, 3, COLOR_BLUE)

def draw_rect_grid(surface, color, rg:RectGrid):
    draw_rect_array(surface, rg.h_rects)
    draw_rect_array(surface, rg.v_rects)
    draw_point(surface, COLOR_BLUE, rg.bbox.bl, 5)

if __name__ == '__main__':
    SCREEN_WIDTH = 500
    SCREEN_HEIGHT = 500
    
    BG_COLOR = (0,0,0,255)
    COLOR_0 = (255, 255, 255, 55)
    COLOR_1 = (150, 150, 150, 255)
    COLOR_2 = (100, 100, 100, 255)
    COLOR_RED = (255,0,0,0)
    COLOR_GREEN = (0,255,0,0)
    COLOR_BLUE = (0,0,255,0)
    
    # pygame setup
    pg.init()
    screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pg.time.Clock()
    running = True
    dt = 0

    canvas = pg.Surface((SCREEN_WIDTH,SCREEN_HEIGHT))
    
    r0 = Rect(50,50,200,50)
    r2 = Rect(r0.xm, r0.ym, 10, 10) 
    r1 = Rect(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, 100, 100)
    
    while running:
        #handle input
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
        keys = pg.key.get_pressed()
        if keys[pg.K_j]:
            r0.translate(0,-10)
            r2.translate(0,-10)
        if keys[pg.K_k]:
            r0.translate(0,10)
            r2.translate(0,10)
        if keys[pg.K_h]:
            r0.translate(-10, 0)
            r2.translate(-10, 0)
        if keys[pg.K_l]:
            r0.translate(10, 0)
            r2.translate(10, 0)
        if keys[pg.K_r]:
            r0.rot90(r0.x0, r0.y0)
            r2.moveTo(r0.xm, r0.ym)
        #render
        canvas.fill(BG_COLOR)
        draw_rect(canvas, r0, 1, COLOR_0)
        draw_rect(canvas, r2, 1, COLOR_0)
        draw_point(canvas, r0.bl, 3, COLOR_0)
        draw_rect(canvas, r1, 1, COLOR_2)
        if rm.rect_contains_point(r1, r0.mm):
            draw_point(canvas, r0.mm, 3, COLOR_RED)
        if rm.rect_crosses_x(r0, r1.x0):
            p0 = Point2D(r1.x0, SCREEN_HEIGHT)
            p1 = Point2D(r1.x0, 0)
            draw_line(canvas, p0, p1, 2, COLOR_RED)
        if rm.rect_crosses_x(r0, r1.x1):
            p0 = Point2D(r1.x1, SCREEN_HEIGHT)
            p1 = Point2D(r1.x1, 0)
            draw_line(canvas, p0, p1, 1, COLOR_RED)
        if rm.rect_crosses_y(r0, r1.y0):
            p0 = Point2D(0, r1.y0)
            p1 = Point2D(SCREEN_WIDTH, r1.y0)
            draw_line(canvas, p0, p1, 2, COLOR_RED)
        if rm.rect_crosses_y(r0, r1.y1):
            p0 = Point2D(0, r1.y1)
            p1 = Point2D(SCREEN_WIDTH, r1.y1)
            draw_line(canvas, p0, p1, 2, COLOR_RED)
        if rm.rect_pass_through_rect_x(r0, r1):
            draw_line(canvas, r1.tl, r1.bl, 2, COLOR_BLUE)
            draw_line(canvas, r1.tr, r1.br, 2, COLOR_BLUE)
        if rm.rect_pass_through_rect_y(r0,r1):
            draw_line(canvas, r1.tl, r1.tr, 2, COLOR_BLUE)
            draw_line(canvas, r1.bl, r1.br, 2, COLOR_BLUE)
        if rm.rect_overlaps_rect(r0, r1):
            draw_rect_fill(canvas, r0, 2, COLOR_0, COLOR_RED)
            draw_rect_fill(canvas, rm.get_overlap_rect(r0,r1), 2, COLOR_RED, COLOR_BLUE)
        if rm.rect_contains_rect(r1, r2):
            draw_rect(canvas, r2, 2, COLOR_RED)

        
        screen.blit(pg.transform.flip(canvas, False, True), (0,0))
        pg.display.flip()
        #handle fsp
        dt = clock.tick(10) / 1000
    pg.quit()
