#include <stdint.h>
#include <stdbool.h>

typedef struct Vec2
{
    int32_t data[2];
}Vec2;

Vec2 vec2_init(int32_t x, int32_t y)
{
    Vec2 v;
    v.data[0] = x;
    v.data[1] = y;
    return v;
}

int32_t vec2_x(Vec2 vec)
{
    return vec.data[0];
}

int32_t vec2_y(Vec2 vec)
{
    return vec.data[0];
}

bool vec2_set_x(Vec2* vec, int32_t x)
{
    vec->data[0] = x;
    return true;
}

bool vec2_set_y(Vec2* vec, int32_t y)
{
    vec->data[1] = y;
    return true;
}

bool vec2_translate(Vec2* vec, Vec2 delta)
{
    vec->data[0] += vec2_x(delta);
    vec->data[1] += vec2_y(delta);
    return true;
}

bool vec2_move_to(Vec2* vec, Vec2 pos)
{
    uint32_t dx = vec2_x(pos) - vec2_x(*vec);
    uint32_t dy = vec2_y(pos) - vec2_y(*vec);
    Vec2 delta = vec2_init(dx, dy);
    vec2_translate(vec, delta); 
    return true;
}

Vec2 vec2_create_copy(Vec2 vec)
{
    Vec2 v;
    v.data[0] = vec2_x(vec);
    v.data[1] = vec2_y(vec);
    return v;
}
