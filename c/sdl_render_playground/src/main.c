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

typedef struct Circle {
  uint16_t center, radius;
}Circle;

//void draw_circle(SDL_Renderer *ap_renderer, Circle a_circle, SDL_Color a_color; uint8_t a_num_points)
//{
//   ; 
//}

void set_render_draw_color(SDL_Renderer *ap_renderer, SDL_Color a_c)
{
    SDL_SetRenderDrawColor(ap_renderer, a_c.r, a_c.g, a_c.b, a_c.a);
}

void render(SDL_Renderer* ap_renderer)
{
    set_render_draw_color(ap_renderer, C_WHITE);
    SDL_Rect background = {0,0,SCREEN_WIDTH, SCREEN_HEIGHT};
    SDL_RenderFillRect(ap_renderer, &background);
    Line l = {0, 0, SCREEN_WIDTH, SCREEN_HEIGHT};
    set_render_draw_color(ap_renderer, C_BLACK);
    //SDL_RenderDrawLine(ap_renderer, l.x0, l.y0, l.x1, l.y1);
    set_render_draw_color(ap_renderer, C_GREY);
    //SDL_RenderDrawPoint(ap_renderer, 10,100);
    set_render_draw_color(ap_renderer, C_BLACK);
    SDL_Point quad[4] = {{10,10},{10,20},{20,10},{20,20}}; 
    SDL_RenderDrawPoints(ap_renderer, quad, 4);
        
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
  return 0;
}
