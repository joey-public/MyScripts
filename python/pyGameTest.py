import pygame as pg
import numpy as np
from Shape import _Shape
from Point2D import Point2D
from Rect import Rect
from RectArrays import RectArray
import xforms as xf

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500
# pygame setup
pg.init()
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pg.time.Clock()
running = True
dt = 0

BG_COLOR = (0,0,0,255)
COLOR_0 = (255, 255, 255, 55)
COLOR_1 = (150, 150, 150, 255)
COLOR_2 = (100, 100, 100, 255)
COLOR_RED = (255,0,0,0)
COLOR_GREEN = (0,255,0,0)
COLOR_BLUE = (0,0,255,0)

canvas = pg.Surface((SCREEN_WIDTH,SCREEN_HEIGHT))

p00 = Point2D(0,0)

r0 = Rect(0,0, 10, 100)
r1 = RectArray(r0, 25, 15, 1, 4)
print(f'{r1}')
print(f'r1.bl_rect: {r1.bl_rect.x0} {r1.bl_rect.y0} {r1.bl_rect.w} {r1.bl_rect.h}\n{r1.bl_rect.getData()}')
print(f'r1.pitch: ({r1.pitch.x}, {r1.pitch.y})')
print(f'r1.spacing: ({r1.dx}, {r1.dy})')

rot90_xform = np.array([[0, -1],
                        [1, 0]])


def draw_point(surface, color, p, width:int):
    pg.draw.circle(surface, color, (p.x, p.y), width)
def draw_line(surface, color, p0, p1):
    pg.draw.line(surface, color, (p0.x, p0.y), (p1.x, p1.y))
def draw_rect(surface, color, r, width=5):
    draw_line(surface, color, r.bl, r.tl)
    draw_line(surface, color, r.tl, r.tr)
    draw_line(surface, color, r.tr, r.br)
    draw_line(surface, color, r.bl, r.br)
def draw_rect2(surface, color, r, width=5):
    draw_point(surface, COLOR_RED, r.bl, width)
    draw_point(surface, color, r.br, width)
    draw_point(surface, color, r.tl, width)
    draw_point(surface, color, r.tr, width)
    draw_rect(surface, color, r)
def draw_rect_x(surface, outline_color, x_color, r):
    draw_rect(surface, outline_color, r)
    draw_line(surface, x_color, r.tl, r.br)
    draw_line(surface, x_color, r.tr, r.bl)
def draw_rect_x2(surface, outline_color, x_color, r):
    draw_rect2(surface, outline_color, r)
    draw_line(surface, x_color, r.tl, r.br)
    draw_line(surface, x_color, r.tr, r.bl)

def draw_rect_array(surface, color, ra:RectArray):
    rect = Rect(ra.bl_rect.x0, ra.bl_rect.y0, ra.bl_rect.w, ra.bl_rect.h)
    for r in range(ra.nrows):
        for c in range(ra.ncols):
            if r==0 and c==0:
                draw_rect_x2(surface, color, color, rect)
            else:
                draw_rect_x(surface, color, color, rect)
            rect.translate(ra.pitch.x, 0)
        rect.translate(-1*int(ra.ncols*ra.pitch.x), ra.pitch.y)

def draw_axis(surface, color, width):
    pg.draw.line(surface, color, (SCREEN_WIDTH/2, 0), (SCREEN_WIDTH/2, SCREEN_HEIGHT), width)
    pg.draw.line(surface, color, (0, SCREEN_HEIGHT/2), (SCREEN_WIDTH, SCREEN_HEIGHT/2), width)

while running:
    #handle input
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    keys = pg.key.get_pressed()
    if keys[pg.K_j]:
        r1.bl_rect.translate(0, -25)    
    if keys[pg.K_k]:
        r1.bl_rect.translate(0, 25)    
    if keys[pg.K_l]:
        r1.bl_rect.translate(25, 0)    
    if keys[pg.K_h]:
        r1.bl_rect.translate(-25, 0)    
    if keys[pg.K_w]:
        r1.bl_rect.moveTo(SCREEN_WIDTH/2-r1.bl_rect.w/2, SCREEN_HEIGHT-r1.bl_rect.h)
    if keys[pg.K_a]:
        r1.bl_rect.moveTo(0, 0)
    if keys[pg.K_r]:
        r1.bl_rect.rot90(r1.bl_rect.x0, r1.bl_rect.y0)
    if keys[pg.K_f]:
        r1.bl_rect.flip(True, False)
    if keys[pg.K_1]:
        r1.nrows = max(r1.nrows - 1, 0)
    if keys[pg.K_2]:
        r1.nrows = min(r1.nrows + 1, 5)
    if keys[pg.K_3]:
        r1.ncols = max(r1.ncols - 1, 0)
    if keys[pg.K_4]:
        r1.ncols = min(r1.ncols + 1, 7)
    if keys[pg.K_b]:
        r1.bl_rect.stretch(1, 2)
    if keys[pg.K_c]:
        r1.bl_rect.stretch(1, 1/2)
        #r1.rot90(r1.xm, r1.ym)
    #render
    canvas.fill(BG_COLOR)
    draw_point(canvas, COLOR_BLUE, p00, 3)
    draw_rect_array(canvas, COLOR_1, r1)
    screen.blit(pg.transform.flip(canvas, False, True), (0,0))
    draw_axis(screen, COLOR_0, 1)
    pg.display.flip()
    #handle fsp
    dt = clock.tick(10) / 1000
pg.quit()
