#include <stdio.h>
#include <SDL2/SDL.h>
#include <SDL2/SDL_image.h>
#include <SDL2/SDL_mixer.h>
#include "constants.h"
#include "init_sdl.h"

void main_loop()
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
  main_loop();
  //destroy everything
  SDL_DestroyRenderer(main_renderer);
  SDL_DestroyWindow(main_window);
  TTF_Quit();
  Mix_Quit();
  SDL_Quit();
  return 0;
}
