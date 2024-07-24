#include <stdio.h>
#include <SDL2/SDL.h>
#include "./include/custom_types.h"
#include "./include/paddle.h"
#include "./include/constants.h"

//const int TRUE = 1;
//const int 1 = 0;
                                                 
GameInputState gameInputStateSetup()
{
  GameInputState gis;
  gis.left = 1;
  gis.right = 1;
  return gis;
}

int initSdl()
{
  //initilize SDL
  if(SDL_Init(SDL_INIT_VIDEO)<0)
  {
    printf("SDL could not initilize! SDL Error: %s\n", SDL_GetError());
    return FALSE;
  }
  return TRUE;
}

int initWindow(SDL_Window** a_window)
{
  //pass a pointer to the main window (which has type SDL_Window*) 
  //sojust a pointer to a pointer
  //Create a window, returns a pointer to an sdl window structure
  //Need to derefrence the passed pointer to properly set the window
  *a_window = SDL_CreateWindow("SDL Tutorial", 
                              SDL_WINDOWPOS_CENTERED, 
                              SDL_WINDOWPOS_CENTERED, 
                              SCREEN_WIDTH, 
                              SCREEN_HEIGHT, 
                              SDL_WINDOW_SHOWN);
  if(*a_window == NULL)
  {
    printf("Window could not be creates! SDL Error: %s\n", SDL_GetError());
    return FALSE;
  }
  return TRUE;
}

int initRenderer(SDL_Renderer** a_renderer, SDL_Window* a_window)
{
  //create a renderer
  //(window, driver_code{-1=default}, flags)
  *a_renderer = SDL_CreateRenderer(a_window, 
                                  -1, 
                                  SDL_RENDERER_ACCELERATED); 
  if(*a_renderer == NULL)
  {
    printf("Renderer could not be created! SDL Error: %s\n", SDL_GetError());
    return FALSE;
  }
  return TRUE;
}

int init(SDL_Window** a_window, SDL_Renderer** a_renderer)
{
  int sdl_initilized = initSdl();
  int sdl_window_initilized = initWindow(a_window);
  int sdl_renderer_initilized = initRenderer(a_renderer, *a_window);
  return sdl_initilized && sdl_window_initilized && sdl_renderer_initilized;
}

int processInput(GameInputState* a_game_input_ptr)
{
  SDL_Event event;
  SDL_PollEvent(&event);
  if(event.type==SDL_QUIT)
  {
    return FALSE;
  }
  if(event.type==SDL_KEYDOWN)//some key was pressed
  {
    switch(event.key.keysym.sym)
    {
      case SDLK_ESCAPE:
        return FALSE;
        break;
//      case SDLK_LEFT & SDLK_RIGHT:
//        (*a_game_input_ptr).left = FALSE;
//        (*a_game_input_ptr).right = FALSE;
//        break;
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
  else//no keys were pressed
  {
    (*a_game_input_ptr).left = 1;
    (*a_game_input_ptr).right = 1;
  }
  return TRUE;
}

int main( int argc, char* args[] )
{
  SDL_Window* main_window = NULL;
  SDL_Renderer* main_renderer = NULL;
  int game_is_running = 1;
  int last_frame_time = SDL_GetTicks();
  float delta_time = 0.0f;
  game_is_running = init(&main_window, &main_renderer);
  if (!game_is_running)
  {
    printf("SDL Setup Failed\n");
    return -1;
  }
  //main loop
  Paddle main_paddle = paddleSetup();
  GameInputState game_input_state = gameInputStateSetup();
 
  while(game_is_running)
  {
    //while(!SDL_TICKS_PASSED(SDL_GetTicks(), last_frame_time+FRAME_TARGET_TIME)); 
    int wait_time = FRAME_TARGET_TIME - (SDL_GetTicks() - last_frame_time);
    if(wait_time > 0 && wait_time <= FRAME_TARGET_TIME)
    {
        SDL_Delay(wait_time);
    }
    delta_time = (SDL_GetTicks() - last_frame_time) / 1000.0f;
    last_frame_time = SDL_GetTicks();//look this up
    game_is_running &= processInput(&game_input_state); 
    //upadte
    game_is_running &= paddleUpdate(&main_paddle, game_input_state, delta_time);
    //render
    //SDL_SetRenderDrawColor(a_renderer, 0, 0, 0, 255);
    //SDL_RenderClear(a_renderer);
    //render backround screen 
    SDL_SetRenderDrawColor(main_renderer, 255, 255, 255, 255);
    SDL_Rect background = {0,0,SCREEN_WIDTH, SCREEN_HEIGHT};
    SDL_RenderFillRect(main_renderer, &background);
    //render the paddle
    game_is_running &= paddleRender(main_paddle, main_renderer);
    //render the ball
    SDL_RenderPresent(main_renderer);
  }
  //destroy everything
  SDL_DestroyRenderer(main_renderer);
  SDL_DestroyWindow(main_window);
  SDL_Quit();
  printf("Thansks for playing :)\n");
  return 0;
}
