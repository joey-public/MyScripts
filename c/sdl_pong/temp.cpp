#include <stdio.h>
#include <string>
#include <SDL2/SDL.h>
//#include <>
//Screen dimension constants
const int SCREEN_WIDTH = 640;
const int SCREEN_HEIGHT = 480;

bool initSdl();
bool initWindow(SDL_Window* a_window);
bool initRenderer(SDL_Renderer* a_renderer, SDL_Window* a_window);
bool loadMedia();
SDL_Texture* loadTexture( std::string path );
bool processInput(); //handle user input, return false iff the game should quit
//Frees media and shuts down SDL
void close();


bool init(SDL_Window* a_window, SDL_Renderer* a_renderer)
{
  bool sdl_initilized = initSdl();
  bool sdl_window_initilized = initWindow(a_window);
  bool sdl_renderer_initilized = initRenderer(a_renderer, a_window);
  return sdl_initilized && sdl_window_initilized && sdl_renderer_initilized;
}

bool initSdl()
{
  //initilize SDL
  if(SDL_Init(SDL_INIT_VIDEO)<0)
  {
    printf("SDL could not initilize! SDL Error: %s\n", SDL_GetError());
    return false;
  }
  return true;
}

bool initWindow(SDL_Window* a_window)
{
  //Create a window, returns a pointer to an sdl window structure
  a_window = SDL_CreateWindow("SDL Tutorial", 
                            SDL_WINDOWPOS_UNDEFINED, 
                            SDL_WINDOWPOS_UNDEFINED, 
                            SCREEN_WIDTH, 
                            SCREEN_HEIGHT, 
                            SDL_WINDOW_SHOWN);
  if(a_window == NULL)
  {
    printf("Window could not be creates! SDL Error: %s\n", SDL_GetError());
    return false;
  }
  return true;
}

bool initRenderer(SDL_Renderer* a_renderer, SDL_Window* a_window)
{
  a_renderer = SDL_CreateRenderer(a_window, 
                                  -1, 
                                  SDL_RENDERER_ACCELERATED); 
  if(a_renderer == NULL)
  {
    printf("Renderer could not be created! SDL Error: %s\n", SDL_GetError());
    return false;
  }
  return true;
}

bool processInput()
{
  while(SDL_PollEvent(&e) != 0)
  {
    if(e.type == SDL_QUIT){ return false; }
  }
  return true;
}

int main( int argc, char* args[] )
{
  SDL_Window* main_window = NULL;
  SDL_Renderer* main_renderer = NULL;
  if(!init(main_window, main_renderer))  
  { 
    printf("Failed to Initilize!\n"); 
    return -1;
  }
  bool exit_game = false;
  while(!exit_game)
  {
    exit_game = processInput();
  }
  return 0;
}
