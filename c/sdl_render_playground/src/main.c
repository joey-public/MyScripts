#include <stdio.h>
#include <math.h>
#include <SDL2/SDL.h>
#include <SDL2/SDL_image.h>
#include <SDL2/SDL_mixer.h>
#include "constants.h"
#include "init_sdl.h"

const SDL_Color C_WHITE= {235,235,235,255};
const SDL_Color C_GREY= {107,107,107,255};
const SDL_Color C_GREY2= {200,200,200,120};
const SDL_Color C_BLACK= {20,20,20,255};

typedef struct Line {
  uint16_t x0, y0, x1, y1;
}Line;

void set_render_draw_color(SDL_Renderer *ap_renderer, SDL_Color a_c)
{
    SDL_SetRenderDrawColor(ap_renderer, a_c.r, a_c.g, a_c.b, a_c.a);
}

void draw_line(SDL_Renderer *ap_renderer, int x0, int y0, int x1, int y1)
{
    int dx, dy, sx, sy, err, e2;
    dx = abs(x1 - x0);
    dy = -abs(y1 - y0); 
    sx = x0 < x1 ? 1 : -1;
    sy = y0 < y1 ? 1 : -1; 
    err = dx + dy; /* error value e_xy */
    for(;;)
    {  
        SDL_RenderDrawPoint(ap_renderer, x0, y0);
        if (x0 == x1 && y0 == y1) break;
        e2 = 2 * err;
        if (e2 >= dy) { err += dy; x0 += sx; } /* e_xy+e_x > 0 */
        if (e2 <= dx) { err += dx; y0 += sy; } /* e_xy+e_y < 0 */
    }
}

void draw_dashed_line(SDL_Renderer *ap_renderer, int x0, int y0, int x1, int y1)
{
    int segment_length, space_length;
}

void draw_rect(SDL_Renderer *ap_renderer, int x, int y, int w, int h)
{
    //draw the horizontal lines
    for(int i = 0; i < w; i++)
    {
        SDL_RenderDrawPoint(ap_renderer, x+i, y);
        SDL_RenderDrawPoint(ap_renderer, x+i, y+h);
    }
    //draw the vertical lines
    for(int i = 0; i < h; i++)
    {
        SDL_RenderDrawPoint(ap_renderer, x, y+i);
        SDL_RenderDrawPoint(ap_renderer, x+w, y+i);
    }
}

void draw_filled_rect(SDL_Renderer *ap_renderer, int x, int y, int w, int h)
{
    //draw the horizontal lines
    for(int i = 0; i < w; i++)
    {
        for(int j = 0; j < h; j++)
        {
            SDL_RenderDrawPoint(ap_renderer, x+i, y+j);
        }
    }
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

void draw_filled_circle(SDL_Renderer *ap_renderer, int center_x, int center_y, int radius) {
    int x = radius;
    int y = 0;
    int error = 0;
    while (x >= y) {
        // Draw horizontal lines to fill the circle
        for (int i = center_x - x; i <= center_x + x; i++) {
            SDL_RenderDrawPoint(ap_renderer, i, center_y + y);
            SDL_RenderDrawPoint(ap_renderer, i, center_y - y);
        }
        for (int i = center_x - y; i <= center_x + y; i++) {
            SDL_RenderDrawPoint(ap_renderer, i, center_y + x);
            SDL_RenderDrawPoint(ap_renderer, i, center_y - x);
        }
        if (error <= 0) {
            y += 1;
            error += 2 * y + 1;
        }
        if (error > 0) {
            x -= 1;
            error -= 2 * x + 1;
        }
    }
}

void draw_ellipse(SDL_Renderer *ap_renderer, int x0, int y0, int x1, int y1)
{
   int a = abs(x1-x0), b = abs(y1-y0), b1 = b&1; /* values of diameter */
   long dx = 4*(1-a)*b*b, dy = 4*(b1+1)*a*a; /* error increment */
   long err = dx+dy+b1*a*a, e2; /* error of 1.step */

   if (x0 > x1) { x0 = x1; x1 += a; } /* if called with swapped points */
   if (y0 > y1) y0 = y1; /* .. exchange them */
   y0 += (b+1)/2; y1 = y0-b1;   /* starting pixel */
   a *= 8*a; b1 = 8*b*b;

   do {
       SDL_RenderDrawPoint(ap_renderer, x1, y0); /*   I. Quadrant */
       SDL_RenderDrawPoint(ap_renderer, x0, y0); /*  II. Quadrant */
       SDL_RenderDrawPoint(ap_renderer, x0, y1); /* III. Quadrant */
       SDL_RenderDrawPoint(ap_renderer, x1, y1); /*  IV. Quadrant */
       e2 = 2*err;
       if (e2 <= dy) { y0++; y1--; err += dy += a; }  /* y step */ 
       if (e2 >= dx || 2*err > dy) { x0++; x1--; err += dx += b1; } /* x step */
   } while (x0 <= x1);
   
   while (y0-y1 < b) {  /* too early stop of flat ellipses a=1 */
       SDL_RenderDrawPoint(ap_renderer, x0-1, y0); /* -> finish tip of ellipse */
       SDL_RenderDrawPoint(ap_renderer, x1+1, y0++); 
       SDL_RenderDrawPoint(ap_renderer, x0-1, y1);
       SDL_RenderDrawPoint(ap_renderer, x1+1, y1--); 
   }
}


void draw_grid(SDL_Renderer *ap_renderer, uint8_t grid_size)
{
  int rows = SCREEN_HEIGHT / grid_size;
  int cols = SCREEN_WIDTH / grid_size;
  SDL_Rect tile_rect;
  tile_rect.x = 0;
  tile_rect.y = 0;
  tile_rect.w = grid_size;
  tile_rect.h = grid_size;
  set_render_draw_color(ap_renderer, C_GREY2);
  for(int i=0; i<rows; i++)
  {
      for(int j=0; j<cols; j++)
      {
          tile_rect.x = j*grid_size;
          tile_rect.y = i*grid_size;
          SDL_RenderDrawRect(ap_renderer, &tile_rect);
      }
  }
}

void draw_map(SDL_Renderer *ap_renderer)
{
  #define TILE_SIZE 32
  #define ROWS 14
  #define COLS 19
  SDL_Rect tile_rect;
  tile_rect.w = TILE_SIZE;
  tile_rect.h = TILE_SIZE;
  uint8_t world_map[ROWS][COLS] = {
      {1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1},
      {1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1},
      {1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1},
      {1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1},
      {1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1},
      {1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1},
      {1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1},
      {1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1},
      {1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1},
      {1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1},
      {1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1},
      {1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1},
      {1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1},
      {1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1},
  };
  //draw the world
  for(int i=0; i<ROWS; i++)
  {
      for(int j=0; j<COLS; j++)
      {
          tile_rect.x = j*TILE_SIZE;
          tile_rect.y = i*TILE_SIZE;
          if(world_map[i][j] == 1)
          {
              SDL_RenderFillRect(ap_renderer, &tile_rect);
          }
      }
  }
}

void render(SDL_Renderer* ap_renderer)
{
    set_render_draw_color(ap_renderer, C_WHITE);
    SDL_RenderClear(ap_renderer);
    SDL_Rect background = {0,0,SCREEN_WIDTH, SCREEN_HEIGHT};
    SDL_RenderFillRect(ap_renderer, &background);
    set_render_draw_color(ap_renderer, C_BLACK);
    draw_line(ap_renderer, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT);
    draw_line(ap_renderer, SCREEN_WIDTH, 0, 0, SCREEN_HEIGHT);
    draw_rect(ap_renderer, 100, 150, 50, 50);
    draw_rect(ap_renderer, 50, 200, 50, 50);
    draw_filled_rect(ap_renderer, 50, 150, 50, 50);
    draw_filled_rect(ap_renderer, 100, 200, 50, 50);
    draw_circle(ap_renderer, 100, 100, 50);
    draw_ellipse(ap_renderer, 400, 100, 450, 300);
    draw_ellipse(ap_renderer, 400, 100, 600, 150);
    int xm, ym; //x and y position of the mouse
    Uint32 buttons = SDL_GetMouseState(&xm, &ym);
    SDL_Rect cursor_point = {xm-1, ym-1, 3, 3};
    SDL_RenderFillRect(ap_renderer, &cursor_point); 
    set_render_draw_color(ap_renderer, C_GREY2);
    draw_circle(ap_renderer, xm, ym, 32);
//    draw_map(ap_renderer);   
    SDL_RenderPresent(ap_renderer);
}

void main_loop(SDL_Renderer *ap_renderer)
{
    uint8_t game_is_running = TRUE;
    while(game_is_running)
    {
       SDL_Event e;
       SDL_PollEvent(&e);
       if(e.type==SDL_QUIT)
       {
            printf("The X button was pressed, Quitting the Game \n");
            game_is_running = FALSE;
       }
       render(ap_renderer);
    }
}

int main(void)
{
  SDL_Window* main_window = NULL;
  SDL_Renderer* main_renderer = NULL;
  if(!initSdl()){return -1;}
  int sdl_initilized = init(&main_window, &main_renderer);
  if(!sdl_initilized){
    printf("SDL Setup Failed\n");
    return -1;
  }
  SDL_SetRenderDrawBlendMode(main_renderer, SDL_BLENDMODE_BLEND); //endables alpha blending
  SDL_ShowCursor(0);//turn off the cursor
  main_loop(main_renderer);
  //destroy everything
  SDL_DestroyRenderer(main_renderer);
  SDL_DestroyWindow(main_window);
  TTF_Quit();
  Mix_Quit();
  SDL_Quit();
  return 0;
}
