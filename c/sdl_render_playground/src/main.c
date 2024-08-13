#include <stdio.h>
#include <SDL2/SDL.h>
#include <SDL2/SDL_image.h>
#include <SDL2/SDL_mixer.h>
#include "constants.h"
#include "init_sdl.h"

const SDL_Color C_WHITE= {235,235,235,255};
const SDL_Color C_GREY= {107,107,107,255};
const SDL_Color C_BLACK= {20,20,20,255};

typedef struct Line {
  uint16_t x0, y0, x1, y1;
}Line;

void set_render_draw_color(SDL_Renderer *ap_renderer, SDL_Color a_c)
{
    SDL_SetRenderDrawColor(ap_renderer, a_c.r, a_c.g, a_c.b, a_c.a);
}

void draw_circle_naive(SDL_Renderer *ap_renderer, float a, float b, float r)
{
    uint8_t xmin = 0;
    uint8_t xmax = SCREEN_WIDTH;
    uint8_t ymin = 0;
    uint8_t ymax = SCREEN_HEIGHT;
    set_render_draw_color(ap_renderer, C_BLACK);
//////////////////    printf("Drawing a circle:\n\tr=%d\n\tx,y=%d,%d\n", r, a, b);
    for(int i = xmin; i < xmax; i++)
    {
        for(int j = ymin; j < ymax; j++)
        {
            //equation of a circle: 0 = (x-a)^2 + (y-b)^2 - r^2
            float fc = (i-a)*(i-a) + (j-b)*(j-b) - r*r;
//            printf("%f\n",fc);
            if(fc <= 0)
            { 
                SDL_RenderDrawPoint(ap_renderer, i, j); 
                printf("Hello\n");
            }
        }
    }
    set_render_draw_color(ap_renderer, C_WHITE);
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
    //draw_map(ap_renderer);   
    draw_circle_naive(ap_renderer, SCREEN_WIDTH/2, SCREEN_HEIGHT/2, 16);
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
