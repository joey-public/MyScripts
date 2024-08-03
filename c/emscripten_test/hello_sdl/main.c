#include <stdio.h>
#include <SDL2/SDL.h>

#ifdef __EMSCRIPTEN__
#include <emscripten.h>
#endif

#define TRUE 1
#define FALSE 0
#define SCREEN_WIDTH 640
#define SCREEN_HEIGHT 480
#define FPS 30

typedef struct LoopArgs{
  SDL_Window* w;
  SDL_Renderer* r;
}LoopArgs;

int init(SDL_Window** a_window, SDL_Renderer** a_renderer)
{
  //initilize SDL
  if(SDL_Init(SDL_INIT_VIDEO | SDL_INIT_AUDIO)<0){
    printf("SDL could not initilize! SDL Error: %s\n", SDL_GetError());
    return FALSE;
  }
  //init the window
  *a_window = SDL_CreateWindow("Game", 
                              SDL_WINDOWPOS_CENTERED, 
                              SDL_WINDOWPOS_CENTERED, 
                              SCREEN_WIDTH, 
                              SCREEN_HEIGHT, 
                              SDL_WINDOW_SHOWN);
  if(*a_window == NULL){
    printf("Window could not be creates! SDL Error: %s\n", SDL_GetError());
    return FALSE;
  }
  //init the renderer
  *a_renderer = SDL_CreateRenderer(*a_window, 
                                  -1, 
                                  SDL_RENDERER_ACCELERATED); 
  if(*a_renderer == NULL){
    printf("Renderer could not be created! SDL Error: %s\n", SDL_GetError());
    return FALSE;
  }
  //init ttf, mixer, ect here as needed
  return TRUE;
}

void main_loop_itr(void* args)
{
  LoopArgs* a = args;
  SDL_Window* a_window = a->w;
  SDL_Renderer* a_renderer = a->r;
  float delta_time = 1.0f/FPS;
  SDL_Rect rect;
  rect.x = 50;
  rect.y = 50;
  rect.w = 50;
  rect.h = 50;
  SDL_Color color = {255,255,255,255};
  SDL_SetRenderDrawColor(a_renderer, color.r, color.g, color.b, color.a);
  SDL_RenderFillRect(a_renderer, &rect);
  SDL_RenderPresent(a_renderer);
}

int main(int argc, char** argv) {
  printf("hello, world!\n");

  SDL_Window* window = NULL;
  SDL_Renderer* renderer = NULL;
  init(&window, &renderer);
  LoopArgs args = {window, renderer};
  int sim_inf_loop = TRUE;
  emscripten_set_main_loop_arg(main_loop_itr, &args, FPS, sim_inf_loop);
  SDL_DestroyRenderer(renderer);
  SDL_DestroyWindow(window);
  SDL_Quit();
  printf("goodbye, world!\n");

  return 0;
}
