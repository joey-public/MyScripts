#include <stdio.h>
#include <stdbool.h>
#include <stdint.h>
#include <SDL2/SDL.h>
#include <SDL2/SDL_image.h>
#include <SDL2/SDL_mixer.h>
#include "init_sdl.h"

#define SCREEN_WIDTH 640
#define SCREEN_HEIGHT 480
#define FPS_TARGET 90 //frames per sec
#define FRAME_TARGET_TIME 1000/FPS_TARGET //ms 

const SDL_Color C_WHITE= {235,235,235,255};
const SDL_Color C_GREY= {107,107,107,255};
const SDL_Color C_GREY2= {200,200,200,0};
const SDL_Color C_BLACK= {20,20,20,255};

void setRenderDrawColor(SDL_Renderer *ap_renderer, SDL_Color a_c)
{
    SDL_SetRenderDrawColor(ap_renderer, a_c.r, a_c.g, a_c.b, a_c.a);
}

void mainSetup(SDL_Renderer *ap_renderer)
{
}

void mainUpdate(SDL_Event *e)
{
}

void mainRender(SDL_Renderer *ap_renderer)
{
    setRenderDrawColor(ap_renderer, C_WHITE);
    SDL_RenderClear(ap_renderer);
    SDL_Rect background = {0,0,SCREEN_WIDTH, SCREEN_HEIGHT};
    SDL_RenderFillRect(ap_renderer, &background);
    setRenderDrawColor(ap_renderer, C_BLACK);
    SDL_RenderFillRect(ap_renderer, &(SDL_Rect){SCREEN_WIDTH/2-25, SCREEN_HEIGHT/2-25, 50, 50});
    SDL_RenderDrawLine(ap_renderer, SCREEN_WIDTH/2, 0, SCREEN_WIDTH/2, SCREEN_HEIGHT);
    SDL_RenderDrawLine(ap_renderer, 0, SCREEN_HEIGHT/2, SCREEN_WIDTH, SCREEN_HEIGHT/2);
    SDL_RenderPresent(ap_renderer);
}

bool iterateMainLoop(SDL_Renderer *ap_renderer, float delta_time)
{
    //handle_input
    SDL_Event e;
    SDL_PollEvent(&e);
    if(e.type==SDL_QUIT)
    {
        printf("The X button was pressed, Quitting the Game \n");
        return false;
    }
    if(e.type == SDL_KEYDOWN)
    {
        switch(e.key.keysym.sym)
        {
            case SDLK_ESCAPE:
                return false;
        }
    }
    mainUpdate(&e);
    mainRender(ap_renderer);
    return true;
}

void mainLoop(SDL_Renderer *ap_renderer)
{
    bool game_is_running = true;
    int last_frame_time = SDL_GetTicks();
    float delta_time = 0.0f;
    while(game_is_running)
    {
        int wait_time = FRAME_TARGET_TIME - (SDL_GetTicks() - last_frame_time); 
        if(wait_time > 0 && wait_time <=FRAME_TARGET_TIME)
        {
            SDL_Delay(wait_time);
        }
        delta_time = (SDL_GetTicks() - last_frame_time) / 1000.0f; 
        last_frame_time = SDL_GetTicks();
        game_is_running = iterateMainLoop(ap_renderer, delta_time);
    }
}

void mainCleanup(SDL_Renderer *ap_renderer, SDL_Window *ap_window)
{
  SDL_DestroyRenderer(ap_renderer);
  SDL_DestroyWindow(ap_window);
  TTF_Quit();
  Mix_Quit();
  SDL_Quit();
}

int main(void)
{
  SDL_Window* main_window = NULL;
  SDL_Renderer* main_renderer = NULL;
  if(!initSdlAudioVideo())
  { 
      return -1;
  }
  int sdl_initilized = initSdl(&main_window, &main_renderer, SCREEN_WIDTH, SCREEN_HEIGHT);
  if(!sdl_initilized)
  {
    printf("SDL Setup Failed\n");
    return -1;
  }
  mainSetup(main_renderer);
  mainLoop(main_renderer);
  mainCleanup(main_renderer, main_window);
  //destroy everything
  return 0;
}
