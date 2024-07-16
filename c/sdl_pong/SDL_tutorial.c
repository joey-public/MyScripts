#include <stdio.h>
#include <SDL2/SDL.h>

//Screen dimension constants
const int SCREEN_WIDTH = 640;
const int SCREEN_HEIGHT = 480;
const int TRUE = 1;
const int FALSE = 0;
const int FPS_TARGET = 60; //frames per sec
const float FRAME_TARGET_TIME = 1000/FPS_TARGET; //ms 

struct ball {
  float x;
  float y;
  float width;
  float height;
} ball;

int init(SDL_Window** a_window, SDL_Renderer** a_renderer);
int initSdl();
int initWindow(SDL_Window** a_window);
int initRenderer(SDL_Renderer**, SDL_Window* a_window);
int setup();
int processInput(); //handle user input, return FALSE iff the game should quit
int update(float a_delta_time);
int render(SDL_Renderer* a_renderer);
//TODO: create close() fucntion that deletes everything

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
  ball.x = 20;
  ball.y = 20;
  ball.width = 15;
  ball.height = 15;
  return TRUE;
}

int processInput()
{
  SDL_Event event;
  SDL_PollEvent(&event);
  switch (event.type)
  {
    case SDL_QUIT: 
      return FALSE;
      break;
    case SDL_KEYDOWN:
      if (event.key.keysym.sym == SDLK_ESCAPE)
      {
        return FALSE;
      }
      break;
  }
  return TRUE;
}

int update(float a_delta_time)
{
  ball.x += 20 * a_delta_time;
  ball.y += 10 * a_delta_time;
  return TRUE;
}

int render(SDL_Renderer* a_renderer)
{
  //args -> (renderer, r, g, b, a)
  SDL_SetRenderDrawColor(a_renderer, 248,248,248,255);
  SDL_RenderClear(a_renderer);
  SDL_Rect ball_rect = {
  (int)ball.x,
  (int)ball.y,
  (int)ball.width,
  (int)ball.height
  };
  SDL_SetRenderDrawColor(a_renderer, 18,18,18,255);
  SDL_RenderFillRect(a_renderer, &ball_rect);
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
