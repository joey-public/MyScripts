#include <stdio.h>
#include <SDL2/SDL.h>
#include <SDL2/SDL_image.h>
#include <SDL2/SDL_mixer.h>
//#include "init_sdl.h"

#define FALSE 0
#define TRUE  1

int main()
{
  SDL_Window* main_window = NULL;
  SDL_Renderer* main_renderer = NULL;
  if(!initSdl()){return -1;}
  int sdl_initilized = init(&main_window, &main_renderer);
  if(!sdl_initilized){
    printf("SDL Setup Failed\n");
    return -1;
  }
  printf("hello world!\n");
  return 0;
}
