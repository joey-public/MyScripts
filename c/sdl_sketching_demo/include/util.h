#ifndef UTIL_H
#define UTIL_H
#include <SDL2/SDL.h>


void set_render_target(SDL_Renderer *ap_renderer, SDL_Texture *ap_texture);

SDL_Texture* load_texture_form_path(SDL_Renderer *ap_renderer, char *path_str);

void set_render_draw_color(SDL_Renderer *ap_renderer, SDL_Color a_c);

void draw_circle(SDL_Renderer *ap_renderer, int xm, int ym, int r);
void draw_texture_circle(SDL_Renderer *ap_renderer, SDL_Texture *ap_texture,int xm, int ym, int r);
void draw_textured_line(SDL_Renderer *ap_renderer, SDL_Texture *ap_texture, int x0, int y0, int x1, int y1, int tex_w, int tex_h);

#endif
