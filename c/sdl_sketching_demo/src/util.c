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

void draw_circle(SDL_Renderer *ap_renderer, int xm, int ym, int r) {
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

