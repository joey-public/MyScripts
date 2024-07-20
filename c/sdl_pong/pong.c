#include <stdio.h>
#include <SDL2/SDL.h>
#include "pong.h"

//TODO setupPaddle(), setupBall, setupWall() functions
//TODO make all game objects provate to main function, not gloabl (maybe use typedef?)
//TODO: create close() fucntion that deletes everything
//TODO: smooth out paddle movement
//TODO: seperate paddle into its own file
//TODO: seperte ball into its own file

//constants
const int SCREEN_WIDTH = 640;
const int SCREEN_HEIGHT = 480;
const int TRUE = 1;
const int FALSE = 0;
const int FPS_TARGET = 90; //frames per sec
const float FRAME_TARGET_TIME = 1000/FPS_TARGET; //ms 
const float PADDLE_SPEED = 2000;
const int PADDLE_MIN_X = 0;
const int PADDLE_MAX_X = SCREEN_WIDTH;
const int PADDLE_WIDTH = 80;
const int PADDLE_HEIGHT = 10;
const int PADDLE_Y_POS = SCREEN_HEIGHT-PADDLE_HEIGHT-10;

//Types
typedef struct fVector2d{
  float x;
  float y;
} fVector2d;

struct paddle {
  SDL_Rect sprite_box;
  fVector2d position;
  int moving_left;
  int moving_right;
  float speed;
} paddle;

struct ball {
  SDL_Rect sprite_box; //the box we render for this simple game its also the collsion box 
  fVector2d position;
  float speed;
} ball;


int init(SDL_Window** a_window, SDL_Renderer** a_renderer)
{
  int sdl_initilized = initSdl();
  int sdl_window_initilized = initWindow(a_window);
  int sdl_renderer_initilized = initRenderer(a_renderer, *a_window);
  return sdl_initilized && sdl_window_initilized && sdl_renderer_initilized;
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

int setup()
{
  ball.sprite_box.x = 20;
  ball.sprite_box.y = 20;
  ball.sprite_box.w = 15;
  ball.sprite_box.h = 15;
  paddle.sprite_box.x = 0;
  paddle.sprite_box.y = PADDLE_Y_POS;
  paddle.sprite_box.w = PADDLE_WIDTH;
  paddle.sprite_box.h = PADDLE_HEIGHT;
  return TRUE;
}

int processInput()
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
      case SDLK_LEFT:
        paddle.moving_left=TRUE;
        paddle.moving_right=FALSE;
        break;
      case SDLK_RIGHT:
        paddle.moving_left=FALSE;
        paddle.moving_right=TRUE;
        break;
      default:
        break;
    }
  }
  else//no keys were pressed
  {
    paddle.moving_left=FALSE;
    paddle.moving_right=FALSE;
  }
  return TRUE;
}

int update(float a_delta_time)
{
  ball.position.x += 40 * a_delta_time;
  ball.position.y += 30 * a_delta_time;
  ball.sprite_box.x = (int)ball.position.x;
  ball.sprite_box.y = (int)ball.position.y;

  if(paddle.moving_left==TRUE && paddle.moving_right==FALSE)
  {
    paddle.position.x -= PADDLE_SPEED * a_delta_time;
    paddle.sprite_box.x = (int) paddle.position.x;
  }
  if(paddle.moving_left==FALSE && paddle.moving_right==TRUE)
  {
    paddle.position.x += PADDLE_SPEED * a_delta_time;
    paddle.sprite_box.x = (int) paddle.position.x;
  }
//  paddle.sprite_box.x = (int)paddle.position.x;
//  paddle.sprite_box.y = (int)paddle.position.y;
  return TRUE;
}

int render(SDL_Renderer* a_renderer)
{
  //args -> (renderer, r, g, b, a)
  SDL_SetRenderDrawColor(a_renderer, 248,248,248,255);
  SDL_RenderClear(a_renderer);

  SDL_SetRenderDrawColor(a_renderer, 18,18,18,255);
  SDL_RenderFillRect(a_renderer, &ball.sprite_box);
  SDL_RenderFillRect(a_renderer, &paddle.sprite_box);
  SDL_RenderPresent(a_renderer);
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
    printf("Setup Failed\n");
    return -1;
  }
  //main loop
  game_is_running = setup();
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
    game_is_running &= processInput(); 
    game_is_running &= update(delta_time);
    game_is_running &= render(main_renderer);
  }
  //destroy everything
  SDL_DestroyRenderer(main_renderer);
  SDL_DestroyWindow(main_window);
  SDL_Quit();
  printf("Thansks for playing :)\n");
  return 0;
}
