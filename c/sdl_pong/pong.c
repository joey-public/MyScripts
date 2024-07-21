#include <stdio.h>
#include <SDL2/SDL.h>
//#include "pong.h"

//TODOs

//constants
const int SCREEN_WIDTH = 640;
const int SCREEN_HEIGHT = 480;
const int TRUE = 1;
const int FALSE = 0;
const int FPS_TARGET = 90; //frames per sec
const float FRAME_TARGET_TIME = 1000/FPS_TARGET; //ms 
//paddle constants                                               
const float PADDLE_SPEED = 2000;
const int PADDLE_MIN_X = 0;
const int PADDLE_MAX_X = 640;
const int PADDLE_WIDTH = 80;
const int PADDLE_HEIGHT = 10;
const int PADDLE_Y_POS = 480-PADDLE_HEIGHT-10;
//ball constants                                               

//typedefs
typedef struct GameInputState{
  int left;
  int right;
  int left_and_right;
  int none;
}GameInputState;

GameInputState GameInputStateSetup()
{
  GameInputState gis;
  gis.left = FALSE;
  gis.right = FALSE;
  return gis;
}

typedef struct Paddle {
  SDL_Rect sprite_box;
  float x_position;
  float y_position;
  float speed;
} Paddle;

Paddle PaddleSetup()
{
  Paddle paddle;
  paddle.sprite_box.x = PADDLE_WIDTH/2;
  paddle.sprite_box.x = PADDLE_Y_POS;
  paddle.sprite_box.w = PADDLE_WIDTH;
  paddle.sprite_box.h = PADDLE_HEIGHT;
  return paddle;
}

typedef struct Ball {
  SDL_Rect sprite_box;
  float x_position;
  float y_position;
  float speed;
}Ball;

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
      case SDLK_LEFT & SDLK_RIGHT:
        (*a_game_input_ptr).left = TRUE;
        (*a_game_input_ptr).right = TRUE;
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
  else//no keys were pressed
  {
    (*a_game_input_ptr).left = FALSE;
    (*a_game_input_ptr).right = FALSE;
  }
  return TRUE;
}

int main( int argc, char* args[] )
{
  SDL_Window* main_window = NULL;
  SDL_Renderer* main_renderer = NULL;
  int game_is_running = FALSE;
  int last_frame_time = SDL_GetTicks();
  float delta_time = 0.0f;
  game_is_running = init(&main_window, &main_renderer);
  if (!game_is_running)
  {
    printf("SDL Setup Failed\n");
    return -1;
  }
  //main loop
  Paddle main_paddle = PaddleSetup();
  GameInputState game_input_state = GameInputStateSetup();
 
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
  }
  //destroy everything
  SDL_DestroyRenderer(main_renderer);
  SDL_DestroyWindow(main_window);
  SDL_Quit();
  printf("Thansks for playing :)\n");
  return 0;
}
