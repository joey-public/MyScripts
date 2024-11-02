import pygame as pg
from Rect import Rect

# pygame setup
pg.init()
screen = pg.display.set_mode((1280, 720))
clock = pg.time.Clock()
running = True
dt = 0

BG_COLOR = (0,0,0,255)
COLOR_0 = (255, 255, 255, 255)
COLOR_1 = (100, 100, 100, 255)

r0 = Rect(100, 100, 100, 100)
r1 = Rect(200, 100, 50, 100)


def draw_rect(surface, color, r:Rect, width=3):
    pg.draw.line(surface, color, r.bl, r.tl, width)
    pg.draw.line(surface, color, r.tl, r.tr, width)
    pg.draw.line(surface, color, r.tr, r.br, width)
    pg.draw.line(surface, color, r.bl, r.br, width)

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
    screen.fill((0,0,0,1))
    draw_rect(screen, COLOR_0, r0) 
    draw_rect_x(screen, COLOR_0, COLOR_1, r1) 
    dx, dy = r0.moveTo(500,300)
    draw_rect_x(screen, COLOR_0, COLOR_1, r0) 

    # flip() the display to put your work on screen
    pg.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(10) / 1000

pg.quit()
