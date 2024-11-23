#include <stdint.h>
#include <stdbool.h>


typedef struct Vec2
{
    int32_t data[2];
}Vec2;

Vec2 vec2_init(int32_t x, int32_t y);
int32_t vec2_x(Vec2 vec);
int32_t vec2_y(Vec2 vec);
bool vec2_set_x(Vec2* vec, int32_t x);
bool vec2_set_y(Vec2* vec, int32_t y);
bool vec2_translate(Vec2* vec, Vec2 delta);
bool vec2_move_to(Vec2* vec, Vec2 pos);
Vec2 vec2_create_copy(Vec2 vec);
