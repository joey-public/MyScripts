#include <stdio.h>
#include <math.h>
#include <SDL2/SDL.h>
#include <SDL2/SDL_image.h>
#include <SDL2/SDL_mixer.h>
#include "constants.h"
#include "init_sdl.h"

const SDL_Color C_WHITE= {235,235,235,255};
const SDL_Color C_GREY= {107,107,107,255};
const SDL_Color C_GREY2= {200,200,200,0};
const SDL_Color C_BLACK= {20,20,20,255};

typedef struct Line {
  uint16_t x0, y0, x1, y1;
}Line;

void set_render_draw_color(SDL_Renderer *ap_renderer, SDL_Color a_c)
{
    SDL_SetRenderDrawColor(ap_renderer, a_c.r, a_c.g, a_c.b, a_c.a);
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

//not working for x1<=x0
void draw_line_naive(SDL_Renderer *ap_renderer, int x0, int y0, int x1, int y1)
{
    int x, y;
    float dx, dy, m;
    dy = y1-y0;
    dx = x1-x0;
    m = dy/dx;
    for(x = x0; x < x1; x++)
    {
        y = round(m*(x-x0)+y0);
        SDL_RenderDrawPoint(ap_renderer, x, y);
    }
}

//implementation of bresenham line algo with floating point math operations
void draw_line_bersenham_float_math(SDL_Renderer *ap_renderer,int x0, int y0, int x1, int y1) 
{
    float b, m, fxy;
    int x, y;
    m = (float) (y1-y0) / (x1-x0);
    b = y0 - m*x0;
    y = y0;
    for(x = x0; x <= x1; x++)
    {
        fxy = m*x - (y+0.5) + b; //find the mindpoint 
        if(fxy > 0)
        {
            y++;
        }
        SDL_RenderDrawPoint(ap_renderer, x, y);
    }

}
void draw_line_bresenham(SDL_Renderer *ap_renderer, int x0, int y0, int x1, int y1)
{
    int dx = x1 - x0;
    int dy = y1 - y0;
    int D = 2*dy - dx;
    //x and y are the current pixel
    int x = x0;
    int y = y0;
    while(x != x1)
    {
        if(D > 0)
        {
            y++;
            D = D + 2*dx;
        }
        else
        {
            D = D - 2*dy;
        }
        SDL_RenderDrawPoint(ap_renderer, x, y);
        x++;
    }
   
}

void test_draw_line_bresenham(SDL_Renderer *ap_renderer)
{
    draw_grid(ap_renderer, 20);
    set_render_draw_color(ap_renderer, C_BLACK);
//  draw_line_bresenham(ap_renderer, 20, 20, 120, 200); //slope = +0.5
//    draw_line_bresenham(ap_renderer, 20, 20, 120, 80); //slope = +1.0
    int x0 = 60;
    int y0 = 60;
    int step = 20;
//    draw_line_naive(ap_renderer, x0, y0, x0-step, y0-step);
//    draw_line_naive(ap_renderer, x0, y0, x0-step, y0);
//    draw_line_naive(ap_renderer, x0, y0, x0-step, y0+step);
//    draw_line_naive(ap_renderer, x0, y0, x0, y0-step);
//    draw_line_naive(ap_renderer, x0, y0, x0, y0+step);
//    draw_line_naive(ap_renderer, x0, y0, x0+step, y0-step);
//    draw_line_naive(ap_renderer, x0, y0, x0+step, y0);
//    draw_line_naive(ap_renderer, x0, y0, x0+step, y0+step);
    draw_line_bersenham_float_math(ap_renderer, x0, y0, x0+step, y0+step);

}


void draw_map(SDL_Renderer *ap_renderer)
{
  #define TILE_SIZE 32
  #define ROWS 14
  #define COLS 19
  #define DRAW_GRID 1
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
              set_render_draw_color(ap_renderer, C_BLACK);
              SDL_RenderFillRect(ap_renderer, &tile_rect);
              set_render_draw_color(ap_renderer, C_WHITE);
          }
          if(DRAW_GRID==TRUE)
          {
              set_render_draw_color(ap_renderer, C_GREY);
              SDL_RenderDrawRect(ap_renderer, &tile_rect);
              set_render_draw_color(ap_renderer, C_WHITE);
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
    test_draw_line_bresenham(ap_renderer);
//    draw_circle_naive(ap_renderer, 100, 100, 50);
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
  main_loop(main_renderer);
  //destroy everything
  SDL_DestroyRenderer(main_renderer);
  SDL_DestroyWindow(main_window);
  TTF_Quit();
  Mix_Quit();
  SDL_Quit();
  return 0;
}
