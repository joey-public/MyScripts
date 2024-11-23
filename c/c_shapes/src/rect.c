#include <stdint.h>
#include <stdbool.h>

typedef struct Rect{
    int32_t data[4];
}Rect;

Rect rect_init(int32_t x, int32_t y, int32_t w, int32_t h)
{
    Rect r;
    r.data[0] = x;
    r.data[1] = x+w;
    r.data[2] = y;
    r.data[4] = y+h;
    return r;
}

int32_t rect_x0(Rect r)
{
    return r.data[0];
}

int32_t rect_x1(Rect r)
{
    return r.data[1];
}

int32_t rect_y0(Rect r)
{
    return r.data[2];
}

int32_t rect_y1(Rect r)
{
    return r.data[3];
}

int32_t rect_w(Rect r)
{
    return rect_x1(r) - rect_x0(r);
}

int32_t rect_h(Rect r)
{
    return rect_y1(r) - rect_y0(r);
}
