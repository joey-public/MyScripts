#include <SDL2/SDL.h>
#include <SDL2/SDL_image.h>
#include "util.h"

void set_render_draw_color(SDL_Renderer *ap_renderer, SDL_Color a_c)
{
    SDL_SetRenderDrawColor(ap_renderer, a_c.r, a_c.g, a_c.b, a_c.a);
}

void set_render_target(SDL_Renderer *ap_renderer, SDL_Texture *ap_texture)
{
    int result = SDL_SetRenderTarget(ap_renderer, ap_texture);
    if(result == -1)
    {
        printf("Error Setting The render Target\n");
    }
}

SDL_Texture* load_texture_form_path(SDL_Renderer *ap_renderer, char *path_str)
{
    SDL_Texture *t = NULL;
    SDL_Surface *s = IMG_Load(path_str); 
    if(s == NULL)
    {
        printf("Unable to load refrece image: %s\n", IMG_GetError());
        return NULL;
    }
    else
    {
        t = SDL_CreateTextureFromSurface(ap_renderer, s);
        if(t == NULL)
        {
            printf("Unable to convert surface to texture: %s\n", SDL_GetError());
            return NULL;
        }
        SDL_FreeSurface(s);
    }
    return t;
}

void draw_circle(SDL_Renderer *ap_renderer, int xm, int ym, int r) 
{
   int x = -r, y = 0, err = 2-2*r; /* II. Quadrant */ 
   do {
      SDL_RenderDrawPoint(ap_renderer, xm-x, ym+y); /*   I. Quadrant */
      SDL_RenderDrawPoint(ap_renderer, xm-y, ym-x); /*  II. Quadrant */
      SDL_RenderDrawPoint(ap_renderer, xm+x, ym-y); /* III. Quadrant */
      SDL_RenderDrawPoint(ap_renderer, xm+y, ym+x); /*  IV. Quadrant */
      r = err;
      if (r <= y) err += ++y*2+1;           /* e_xy+e_y < 0 */
      if (r > x || err > y) err += ++x*2+1; /* e_xy+e_x > 0 or no 2nd y-step */
   } while (x < 0);
}

void draw_texture_circle(SDL_Renderer *ap_renderer, SDL_Texture *ap_texture,int xm, int ym, int r) 
{
   int x = -r, y = 0, err = 2-2*r; /* II. Quadrant */ 
   SDL_Rect dest_rect;
   dest_rect.w = 2;
   dest_rect.h = 2;
   do {
      dest_rect.x = xm-x;
      dest_rect.y = ym+y;
      SDL_RenderCopy(ap_renderer, ap_texture, NULL, &dest_rect);
      dest_rect.x = xm-y;
      dest_rect.y = ym-x;
      SDL_RenderCopy(ap_renderer, ap_texture, NULL, &dest_rect);
      dest_rect.x = xm+x;
      dest_rect.y = ym-y;
      SDL_RenderCopy(ap_renderer, ap_texture, NULL, &dest_rect);
      dest_rect.x = xm+y;
      dest_rect.y = ym+x;
      SDL_RenderCopy(ap_renderer, ap_texture, NULL, &dest_rect);
      r = err;
      if (r <= y) err += ++y*2+1;           /* e_xy+e_y < 0 */
      if (r > x || err > y) err += ++x*2+1; /* e_xy+e_x > 0 or no 2nd y-step */
   } while (x < 0);
}

void draw_textured_line(SDL_Renderer *ap_renderer, SDL_Texture *ap_texture, int x0, int y0, int x1, int y1, int tex_w, int tex_h)
{
    SDL_Rect dest_rect;
    int dx, dy, sx, sy, err, e2;
    dest_rect.w = tex_w;
    dest_rect.h = tex_h;
    dx = abs(x1 - x0);
    dy = -abs(y1 - y0); 
    sx = x0 < x1 ? 1 : -1;
    sy = y0 < y1 ? 1 : -1; 
    err = dx + dy; /* error value e_xy */
    for(;;)
    {  
        //SDL_RenderDrawPoint(ap_renderer, x0, y0);
        dest_rect.x = x0-dest_rect.w/2;
        dest_rect.y = y0-dest_rect.h/2;
        SDL_RenderCopy(ap_renderer, ap_texture, NULL, &dest_rect);
        if (x0 == x1 && y0 == y1) break;
        e2 = 2 * err;
        if (e2 >= dy) { err += dy; x0 += sx; } /* e_xy+e_x > 0 */
        if (e2 <= dx) { err += dx; y0 += sy; } /* e_xy+e_y < 0 */
    }
}
