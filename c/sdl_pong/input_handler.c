#include "./include/input_handler.h"
#include "./include/constants.h"

GameInputState gameInputStateSetup()
{
  GameInputState gis;
  gis.left = 1;
  gis.right = 1;
  return gis;
}

int processInput(GameInputState* a_game_input_ptr)
{
  SDL_Event event;
  SDL_PollEvent(&event);
  if(event.type==SDL_QUIT){
    return FALSE;
  }
  if(event.type==SDL_KEYDOWN){//some key was pressed
    switch(event.key.keysym.sym){
      case SDLK_ESCAPE:
        return FALSE;
        break;
      case SDLK_LEFT:
        (*a_game_input_ptr).left = TRUE;
        (*a_game_input_ptr).right = FALSE;
        break;
      case SDLK_RIGHT:
        (*a_game_input_ptr).left= FALSE;
        (*a_game_input_ptr).right = TRUE;
        break;
      default:
        break;
    }
  }
  else{//no keys were pressed
    (*a_game_input_ptr).left = 1;
    (*a_game_input_ptr).right = 1;
  }
  return TRUE;
}
