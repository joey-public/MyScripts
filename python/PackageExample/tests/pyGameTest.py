import pygame as pg
import numpy as np
from .jShapes import shapes

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

r1 = Rect(10,10, 80, 50)

rot90_xform = np.array([[0, -1],
                        [1, 0]])


def draw_point(surface, color, p:Point2D, width:int):
    pg.draw.circle(surface, color, (p.x, p.y), width)
def draw_line(surface, color, p0:Point2D, p1:Point2D):
    pg.draw.line(surface, color, (p0.x, p0.y), (p1.x, p1.y))
def draw_rect(surface, color, r:Rect, width=5):
    draw_line(surface, color, r.bl, r.tl)
    draw_line(surface, color, r.tl, r.tr)
    draw_line(surface, color, r.tr, r.br)
    draw_line(surface, color, r.bl, r.br)
def draw_rect2(surface, color, r:Rect, width=5):
    draw_point(surface, COLOR_RED, r.bl, width)
    draw_point(surface, color, r.br, width)
    draw_point(surface, color, r.tl, width)
    draw_point(surface, color, r.tr, width)
    draw_rect(surface, color, r)
def draw_rect_x(surface, outline_color, x_color, r:Rect):
    draw_rect(surface, outline_color, r)
    draw_line(surface, x_color, r.tl, r.br)
    draw_line(surface, x_color, r.tr, r.bl)

def draw_axis(surface, color, width):
    pg.draw.line(surface, color, (SCREEN_WIDTH/2, 0), (SCREEN_WIDTH/2, SCREEN_HEIGHT), width)
    pg.draw.line(surface, color, (0, SCREEN_HEIGHT/2), (SCREEN_WIDTH, SCREEN_HEIGHT/2), width)

while running:
    #handle input
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    keys = pg.key.get_pressed()
    if keys[pg.K_r]:
        res = np.matmul(rot90_xform, v0.raw_data[:,1])
    #render
    canvas.fill(BG_COLOR)
    draw_point(canvas, COLOR_BLUE, p00, 3)
    #draw_rect_x(canvas, COLOR_1, COLOR_2, r1) 
    screen.blit(pg.transform.flip(canvas, False, True), (0,0))
    draw_axis(screen, COLOR_0, 1)
    pg.display.flip()
    #handle fsp
    dt = clock.tick(10) / 1000
pg.quit()
