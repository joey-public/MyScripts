#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>
#include <SDL2/SDL.h>
#include <SDL2/SDL_image.h>
#include <SDL2/SDL_mixer.h>
#include "constants.h"
#include "init_sdl.h"
#include "util.h"

const SDL_Color C_WHITE= {235,235,235,255};
const SDL_Color C_GREY= {107,107,107,255};
const SDL_Color C_GREY2= {200,200,200,0};
const SDL_Color C_BLACK= {20,20,20,255};

const uint8_t TOOL_2H_PENCIL = 0;
const uint8_t TOOL_HB_PENCIL = 1;
const uint8_t TOOL_2B_PENCIL = 2;
const uint8_t TOOL_ERASER = 3;
const uint8_t ZOOM_MODE_IN = 0;
const uint8_t ZOOM_MODE_OUT = 1;
const uint8_t GRID_MODE_OFF = 0;
const uint8_t GRID_MODE_ON = 1;
const uint8_t WIDTH_MODE_THIN = 0;
const uint8_t WIDTH_MODE_THICK = 1;

typedef struct Globals {
    SDL_Texture *drawing_texture;
    SDL_Texture *grid_texture;
    SDL_Texture *refrence_texture; 
    uint8_t tool_type;
    uint8_t zoom_mode;
    uint8_t grid_mode;
    uint8_t tool_width;
}Globals;

Globals g_state;

bool create_empty_sdl_texture(SDL_Renderer *ap_renderer, SDL_Texture *t, int width, int height)
{
    if(t!=NULL)
    {
        return false;
    }
    uint32_t fmt = SDL_PIXELFORMAT_RGBA8888;
    int access = SDL_TEXTUREACCESS_TARGET;
    t = SDL_CreateTexture(ap_renderer, fmt, access, width, height); 
    if(t == NULL)
    {
         return false;
    }
    return true;
}

void setup(SDL_Renderer *ap_renderer)
{
    create_empty_sdl_texture(ap_renderer, g_state.drawing_texture, SCREEN_WIDTH, SCREEN_HEIGHT); 
    create_empty_sdl_texture(ap_renderer, g_state.grid_texture, SCREEN_WIDTH, SCREEN_HEIGHT); 
    g_state.refrence_texture = NULL;
    g_state.tool_type = TOOL_2H_PENCIL;
    g_state.zoom_mode = ZOOM_MODE_OUT;
    g_state.grid_mode = GRID_MODE_OFF;
    g_state.tool_width = WIDTH_MODE_THIN;
    SDL_ShowCursor(0);//turn off the cursor
}

void update(SDL_Event *e)
{
    if(e==0){return;}//just return if there was no input this frame
    if(e->type==SDL_KEYDOWN)
    {
        switch(e->key.keysym.sym)
        {
            case SDLK_w:
               g_state.tool_width = !g_state.tool_width; 
               break;
            case SDLK_a:
               g_state.tool_type = TOOL_2H_PENCIL; 
               break;
            case SDLK_s:
               g_state.tool_type = TOOL_HB_PENCIL; 
               break;
            case SDLK_d:
               g_state.tool_type = TOOL_2B_PENCIL; 
               break;
            case SDLK_e:
               g_state.tool_type = TOOL_ERASER; 
               break;
            case SDLK_g:
               g_state.grid_mode = !g_state.grid_mode; 
               break;
        }
    }
}

void render(SDL_Renderer *ap_renderer)
{
    //render the background
    set_render_draw_color(ap_renderer, C_WHITE);
    SDL_RenderClear(ap_renderer);
    SDL_Rect background = {0,0,SCREEN_WIDTH, SCREEN_HEIGHT};
    SDL_RenderFillRect(ap_renderer, &background);
    //render the cursor
    set_render_draw_color(ap_renderer, C_BLACK);
    int xm, ym; //x and y position of the mouse
    Uint32 buttons = SDL_GetMouseState(&xm, &ym);
    SDL_Rect cursor_point = {xm-1, ym-1, 3, 3};
    SDL_RenderFillRect(ap_renderer, &cursor_point); 
    set_render_draw_color(ap_renderer, C_GREY2);
    draw_circle(ap_renderer, xm, ym, 32);
    //render grid
    if(g_state.grid_mode==GRID_MODE_ON)
    {
        set_render_draw_color(ap_renderer, C_GREY2);
        int grid_size = 80;
        SDL_SetRenderTarget(ap_renderer, g_state.grid_texture);
        for(int i = 0; i < SCREEN_WIDTH; i+=grid_size)
        {
            SDL_RenderDrawLine(ap_renderer, i, 0, i, SCREEN_HEIGHT);
        }
        for(int i = 0; i < SCREEN_HEIGHT; i+=grid_size)
        {
            SDL_RenderDrawLine(ap_renderer, 0, i, SCREEN_WIDTH, i);
        }
    }
    //render drawing on bottom screen
    SDL_SetRenderTarget(ap_renderer, g_state.drawing_texture);
    set_render_draw_color(ap_renderer, C_BLACK);

    //render the texures
    SDL_SetRenderTarget(ap_renderer, NULL);
    SDL_RenderCopy(ap_renderer, g_state.grid_texture, NULL, NULL);
    SDL_RenderCopy(ap_renderer, g_state.drawing_texture, NULL, NULL);
    
    //swap screen buffers
    SDL_RenderPresent(ap_renderer);
}

bool iterate_main_loop(SDL_Renderer *ap_renderer, float delta_time)
{
    //handle_input
    SDL_Event e;
    SDL_PollEvent(&e);
    if(e.type==SDL_QUIT)
    {
        printf("The X button was pressed, Quitting the Game \n");
        return false;
    }
    if(e.type == SDL_KEYDOWN)
    {
        switch(e.key.keysym.sym)
        {
            case SDLK_ESCAPE:
                return false;
        }
    }
    update(&e);
    render(ap_renderer);
    return true;
}

void main_loop(SDL_Renderer *ap_renderer)
{
    bool game_is_running = true;
    int last_frame_time = SDL_GetTicks();
    float delta_time = 0.0f;
    while(game_is_running)
    {
        int wait_time = FRAME_TARGET_TIME - (SDL_GetTicks() - last_frame_time); 
        if(wait_time > 0 && wait_time <=FRAME_TARGET_TIME)
        {
            SDL_Delay(wait_time);
        }
        delta_time = (SDL_GetTicks() - last_frame_time) / 1000.0f; 
        last_frame_time = SDL_GetTicks();
        game_is_running = iterate_main_loop(ap_renderer, delta_time);
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
  setup(main_renderer);
  main_loop(main_renderer);
  //destroy everything
  SDL_DestroyTexture(g_state.drawing_texture);
  SDL_DestroyTexture(g_state.grid_texture);
  SDL_DestroyRenderer(main_renderer);
  SDL_DestroyWindow(main_window);
  TTF_Quit();
  Mix_Quit();
  SDL_Quit();
  return 0;
}
