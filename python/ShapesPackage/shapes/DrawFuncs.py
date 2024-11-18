from .Point2D import Point2D
from .Rect import Rect
from .RectArray import RectArray
from .RectGrid import RectGrid
from .ShapeContainer import ShapeContainer

def drawPoint(surface, p:Point2D, **kwargs):
    radius = 3
    outline_color = (255,255,255)
    if 'radius' in kwargs.keys(): radius = kwargs['radius']
    if 'outline_color' in kwargs.keys(): outline_color = kwargs['outline_color']
    pg.draw.circle(surface, outline_color, (p.x, p.y), radius)

def drawLine(surface, p0, p1, line_width:int, color:tuple):
    if p0 is None or p1 is None: return 
    pg.draw.line(surface, color, (p0.x, p0.y), (p1.x, p1.y), line_width)

def drawRect(surface:pg.Surface, r:Rect, **kwargs)->None:
    outline_color:tuple = (255,255,255)
    outline_width:float = 1
    fill_color:tuple = None 
    fill_pattern:str = None #x, *, _, |
    fill_pattern_width:float = 1
    fill_pattern_color:tuple = (200,200,200)    
    if 'outline_color' in kwargs.keys(): outline_color = kwargs['outline_color']
    if 'outline_width' in kwargs.keys(): outline_width = kwargs['outline_width']
    if 'fill_color' in kwargs.keys(): fill_color = kwargs['fill_color']
    if 'fill_pattern' in kwargs.keys(): fill_pattern = kwargs['fill_pattern']
    if 'fill_pattern_width' in kwargs.keys(): fill_pattern_width = kwargs['fill_pattern_width']
    if 'fill_pattern_color' in kwargs.keys(): fill_pattern_color = kwargs['fill_pattern_color']
    if not(fill_color is None):
        pg.draw.rect(surface, fill_color, pg.Rect(r.x0, r.y0, r.w, r.h))
    if fill_pattern=='x':
        drawLine(surface, r.bl, r.tr, fill_pattern_width, fill_pattern_color)
        drawLine(surface, r.br, r.tl, fill_pattern_width, fill_pattern_color)
    if fill_pattern=='+':
        drawLine(surface, r.ml, r.mr, fill_pattern_width, fill_pattern_color)
        drawLine(surface, r.mt, r.mb, fill_pattern_width, fill_pattern_color)
    if fill_pattern=='*':
        drawLine(surface, r.bl, r.tr, fill_pattern_width, fill_pattern_color)
        drawLine(surface, r.br, r.tl, fill_pattern_width, fill_pattern_color)
        drawLine(surface, r.ml, r.mr, fill_pattern_width, fill_pattern_color)
        drawLine(surface, r.mt, r.mb, fill_pattern_width, fill_pattern_color)
    if fill_pattern=='_':
        p0 = Point2D(r.x0, r.y0)
        p1 = Point2D(r.x1, r.y0)
        N = 10
        dy = r.h/N
        for i in range(N):
            drawLine(surface, p0, p1, fill_pattern_width, fill_pattern_color)
            p0.translate(0,dy)
            p1.translate(0,dy)
    if fill_pattern=='|':
        p0 = Point2D(r.x0, r.y0)
        p1 = Point2D(r.x0, r.y1)
        N = 10
        dx = r.w/N
        for i in range(N):
            drawLine(surface, p0, p1, fill_pattern_width, fill_pattern_color)
            p0.translate(dx, 0)
            p1.translate(dx, 0)
    #draw the rect outline
    drawLine(surface, r.bl, r.tl, outline_width, outline_color)
    drawLine(surface, r.tl, r.tr, outline_width, outline_color)
    drawLine(surface, r.tr, r.br, outline_width, outline_color)
    drawLine(surface, r.bl, r.br, outline_width, outline_color)


def drawRectArray(surface, ra:RectArray, **kwargs):
    rect = Rect(ra.r0.x0, ra.r0.y0, ra.r0.w, ra.r0.h)
    for r in range(ra.nrows):
        for c in range(ra.ncols):
            drawRect(surface, rect, **kwargs)
            rect.translate(ra.pitch.x, 0)
        rect.translate(-1*int(ra.ncols*ra.pitch.x), ra.pitch.y)

#def drawRectGrid(surface, rg:RectGrid, width0, width1, color):
#    if rg is None: return 
#    draw_rect_array(surface, rg.h_rects, width0, color)
#    draw_rect_array(surface, rg.v_rects, width0, color)
#    draw_rect_array(surface, rg.o_rects, width1, color)

def drawShapeContainer(surface:pg.Surface, c:ShapeContainer, **kwargs):
    for shape in c._shape_list:
        shape_type = type(shape) 
        if shape_type == Point2D:
            draw_point(surface, shape, **kwargs)
        if shape_type == Rect:
            draw_rect(surface, shape, **kwargs)
        if shape_type == RectArray:
            draw_rect_array(surface, shape, **kwargs)
#        if shape_type == RectGrid:
#            draw_rect_grid(surface, shape, **kwargs)

def drawText(surface:pg.Surface, text:str, pos:Point2D, **kwargs):
    font_type = 'Open Sans'
    font_size = 24 
    font_color = (255,255,255)
    aa = True
    if 'font' in kwargs.keys(): 
        font_type = kwargs['font']
    if 'font_size' in kwargs.keys(): 
        font_size = kwargs['font_size']
    if 'font_color' in kwargs.keys(): 
        font_color = kwargs['font_color']
    font = pg.font.SysFont(font_type, font_size)
    label = font.render(text, aa, font_color)
    surface.blit(label, (pos.x, pos.y))
