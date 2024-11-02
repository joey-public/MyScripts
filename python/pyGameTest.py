import pygame as pg
import numpy as np
from Rect import Rect

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

canvas = pg.Surface((SCREEN_WIDTH,SCREEN_HEIGHT))

r1 = Rect(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, 80, 50)

rot90_xform = np.array([[0, -1],
                        [1, 0]])

def rotate_box(angle, box):
    xform = np.array([[np.cos(angle), -np.sin(angle)],
                      [np.sin(angle),  np.cos(angle)]])
    box._applyXformAboutOrigin(xform)

def draw_axis(surface, color, width):
    pg.draw.line(surface, color, (SCREEN_WIDTH/2, 0), (SCREEN_WIDTH/2, SCREEN_HEIGHT), width)
    pg.draw.line(surface, color, (0, SCREEN_HEIGHT/2), (SCREEN_WIDTH, SCREEN_HEIGHT/2), width)

def draw_rect(surface, color, r:Rect, width=5):

    pg.draw.circle(surface, color, r.bl, width)
    pg.draw.line(surface, color, r.bl, r.tl)
    pg.draw.line(surface, color, r.tl, r.tr)
    pg.draw.line(surface, color, r.tr, r.br)
    pg.draw.line(surface, color, r.bl, r.br)

def draw_rect_x(surface, outline_color, x_color, r:Rect):
    draw_rect(surface, outline_color, r)
    pg.draw.line(surface, x_color, r.tl, r.br)
    pg.draw.line(surface, x_color, r.tr, r.bl)

while running:
    # poll for events
    # pg.QUIT event means the user clicked X to close your window
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    # fill the screen with a color to wipe away anything from last frame
    canvas.fill(BG_COLOR)
    draw_axis(canvas, COLOR_0, 1)
    draw_rect_x(canvas, COLOR_1, COLOR_2, r1) 

    screen.blit(pg.transform.flip(canvas, False, True), (0,0))

    keys = pg.key.get_pressed()
    if keys[pg.K_r]:
        r1.applyXformAboutPoint(rot90_xform, r1.bl)
    if keys[pg.K_j]:
        print(f'Rect: {r1.x0}, {r1.y0}, {r1.w}, {r1.h}') 
        print(f'x0+w/2 = {r1.x0+r1.w/2}')
        print(f'y0+h/2 = {r1.y0+r1.h/2}')
        print(f'Rect Center: {r1.cc}') 
        r1.applyXformAboutPoint(rot90_xform, r1.cc)
    # flip() the display to put your work on screen
    pg.display.flip()
    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(10) / 1000


pg.quit()
