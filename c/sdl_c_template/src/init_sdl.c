#include <SDL2/SDL.h>
#include <SDL2/SDL_mixer.h>
#include <SDL2/SDL_ttf.h>
#include <stdbool.h>
#include <stdint.h>
#include "init_sdl.h"

#define MIXER_FS 44000

bool initSdlAudioVideo()
{
  //initilize SDL
  if(SDL_Init(SDL_INIT_VIDEO | SDL_INIT_AUDIO)<0){
    printf("SDL could not initilize! SDL Error: %s\n", SDL_GetError());
    return false;
  }
  return true;
}

bool initMixer(int a_sampe_rate)
{
  if( Mix_OpenAudio(a_sample_rate, MIX_DEFAULT_FORMAT, 2, 2048) < 0){
    printf("SDL_mixer could not initialize! SDL_mixer Error: %s\n", Mix_GetError()); 
    return false;
  }
  return true;
}

bool initTTF()
{
  if(TTF_Init()==-1){
    printf( "SDL_ttf could not initialize! SDL_ttf Error: %s\n", TTF_GetError() );
    return false;    
  }
  return true;
}

bool initWindow(SDL_Window** a_window, uint16_t a_window_width, uint16_t a_window_height)
{
  //pass a pointer to the main window (which has type SDL_Window*) 
  //sojust a pointer to a pointer
  //Create a window, returns a pointer to an sdl window structure
  //Need to derefrence the passed pointer to properly set the window
  *a_window = SDL_CreateWindow("Pong Game", 
                              SDL_WINDOWPOS_CENTERED, 
                              SDL_WINDOWPOS_CENTERED, 
                              a_window_width, 
                              a_window_height, 
                              SDL_WINDOW_SHOWN);
  if(*a_window == NULL){
    printf("Window could not be creates! SDL Error: %s\n", SDL_GetError());
    return false;
  }
  return true;
}

bool initRenderer(SDL_Renderer** a_renderer, SDL_Window* a_window){
  *a_renderer = SDL_CreateRenderer(a_window, 
                                  -1, 
                                  SDL_RENDERER_ACCELERATED); 
  if(*a_renderer == NULL){
    printf("Renderer could not be created! SDL Error: %s\n", SDL_GetError());
    return false;
  }
  return true;
}

bool initSdl(SDL_Window** a_window, SDL_Renderer** a_renderer, uint16_t a_window_width, uint16_t a_window_height)
{
  int sdl_initilized = initSdlAudioVideo();
  int sdl_mixer_initilized = initMixer(MIXER_FS);
  int sdl_ttf_initilized = initTTF();
  int sdl_window_initilized = initWindow(a_window, a_window_width, a_window_height);
  int sdl_renderer_initilized = initRenderer(a_renderer, *a_window);
  return sdl_initilized &&sdl_mixer_initilized && sdl_ttf_initilized && sdl_window_initilized && sdl_renderer_initilized;
}

