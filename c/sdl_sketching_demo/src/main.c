#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>
#include <SDL2/SDL.h>
#include <SDL2/SDL_image.h>
#include <SDL2/SDL_mixer.h>
#include "init_sdl.h"
#include "util.h"

#define CANVAS_WIDTH 320
#define CANVAS_HEIGHT 240
#define CANVAS_SCALE_FACTOR 8 //scale up the canvas for drawing. Scale it down befor rendering
#define BRUSH_W 16
#define BRUSH_H 16
#define BORDER_WIDTH 25//px
#define SCREEN_SEPERATION 5//px
#define REFRENCE_SCREEN_X BORDER_WIDTH
#define REFRENCE_SCREEN_Y BORDER_WIDTH
#define WINDOW_WIDTH 2*BORDER_WIDTH + REFRENCE_SCREEN_WIDTH
#define WINDOW_HEIGHT 2*BORDER_WIDTH + SCREEN_SEPERATION + REFRENCE_SCREEN_HEIGHT + CANVAS_HEIGHT

#define FPS_TARGET 240
#define FRAME_TARGET_TIME 1000/FPS_TARGET

#define TOOL_2H_PENCIL 0
#define TOOL_HB_PENCIL 1
#define TOOL_2B_PENCIL 2
#define TOOL_ERASER 3

#define GRID_SIZE 40//px
                       
const int REFRENCE_SCREEN_WIDTH = CANVAS_WIDTH * 1.5;
const int REFRENCE_SCREEN_HEIGHT = CANVAS_HEIGHT * 1.5;
const int CANVAS_X = BORDER_WIDTH + REFRENCE_SCREEN_WIDTH/2 - CANVAS_WIDTH/2; 
const int CANVAS_Y = BORDER_WIDTH + SCREEN_SEPERATION + REFRENCE_SCREEN_HEIGHT;

const SDL_Color C_WHITE = {235,235,235,255};
const SDL_Color C_GREY = {164,164,164,255};
const SDL_Color C_GREY2 = {92,92,92,255};
const SDL_Color C_BLACK = {20,20,20,255};
const SDL_Color C_ALPHA = {0,0,0,0};

#define  ZOOM_MODE_IN 0
#define  ZOOM_MODE_OUT 1
#define  ZOOM_SCALE 2

#define  GRID_MODE_OFF 1
#define  GRID_MODE_ON 1

#define  WIDTH_MODE_THIN 0
#define  WIDTH_MODE_THICK 1

#define  REF_MODE_IMG 0
#define  REF_MODE_DRAW 1

#define  SCROLL_DIR_NONE 0
#define  SCROLL_DIR_UP 1
#define  SCROLL_DIR_DOWN 2
#define  SCROLL_DIR_LEFT 3
#define  SCROLL_DIR_RIGHT 4
#define  SCROLL_SPEED 4

typedef struct Globals {
    SDL_Texture *drawing_texture; //drawing that can be displayed over the top or bottom screen
    SDL_Texture *grid_texture; //grid that can be displayed over the top or bottom screen
    SDL_Texture *refrence_texture; //hold a refrence image you can try to draw
    SDL_Texture *backround_texture;//gets drawn first behind everything else 
    SDL_Texture *brush_texture;//the texture for the brush
    uint8_t tool_type;
    uint8_t zoom_mode;
    uint8_t ref_mode;
    uint8_t grid_mode;
    uint8_t tool_width;
    uint8_t scoll_direction;
    SDL_Rect zoom_rect;
    bool pen_down;
    int xmo, ymo;
}Globals;

Globals g_state;

bool point_is_in_draw_area(int x, int y)
{
    int xmin = CANVAS_X;
    int xmax = CANVAS_X + CANVAS_WIDTH;
    int ymin = CANVAS_Y;
    int ymax = CANVAS_Y + CANVAS_HEIGHT;
    return (x > xmin & x < xmax & y > ymin & y < ymax);
}

void draw_grid(SDL_Renderer *ap_renderer, int grid_size)
{
    //vertical gridlines
    for(int i = 0; i <= CANVAS_WIDTH; i+=grid_size)
    {
        SDL_RenderDrawLine(ap_renderer, i, 0, i, CANVAS_HEIGHT);
    }
    SDL_RenderDrawLine(ap_renderer, CANVAS_WIDTH-1, 0, CANVAS_WIDTH-1, CANVAS_HEIGHT);
    //vertical gridlines
    for(int i = 0; i <= CANVAS_HEIGHT; i+=grid_size)
    {
        SDL_RenderDrawLine(ap_renderer, 0, i, CANVAS_WIDTH, i);
    }
    SDL_RenderDrawLine(ap_renderer, 0, CANVAS_HEIGHT-1, CANVAS_WIDTH, CANVAS_HEIGHT-1);
}

void draw_cursor(SDL_Renderer *ap_renderer, int a_circle_r, SDL_Color a_point_color, SDL_Color a_circle_color)
{
    int xm, ym; //x and y position of the mouse
     SDL_GetMouseState(&xm, &ym);
    if(point_is_in_draw_area(xm, ym))
    {
        SDL_ShowCursor(0);//turn off the cursor
        SDL_Rect cursor_point = {xm-1, ym-1, 3, 3};
        set_render_draw_color(ap_renderer, a_point_color);
        SDL_RenderFillRect(ap_renderer, &cursor_point); 
        set_render_draw_color(ap_renderer, a_circle_color);
        draw_circle(ap_renderer, xm, ym, a_circle_r);
        //draw_texture_circle(ap_renderer, g_state.refrence_texture, xm, ym, a_circle_r);
    }
    else
    {
        SDL_ShowCursor(1);
    }
}

void draw_pen_stroke(SDL_Renderer *ap_renderer)
{
    switch(g_state.tool_type)
    {
        case TOOL_2H_PENCIL:
            set_render_draw_color(ap_renderer, C_GREY);
            break;
        case TOOL_HB_PENCIL:
            set_render_draw_color(ap_renderer, C_GREY2);
            break;
        case TOOL_2B_PENCIL:
            set_render_draw_color(ap_renderer, C_BLACK);
            break;
        case TOOL_ERASER:
            set_render_draw_color(ap_renderer, C_ALPHA);
            break;
    }
    int xm ,ym, x0, y0, x1, y1;
    float scale;
    SDL_GetMouseState(&xm, &ym);
    //convert the mouse position in the main window to a local x,y values on the smaller drawing texture
    x0 = g_state.xmo - CANVAS_X;
    x1 = xm - CANVAS_X;
    y0 = g_state.ymo - CANVAS_Y;
    y1 = ym - CANVAS_Y;
    //scale up the x,y pos to the larger virtual canvas size
    x0 = x0 * CANVAS_SCALE_FACTOR;
    y0 = y0 * CANVAS_SCALE_FACTOR;
    x1 = x1 * CANVAS_SCALE_FACTOR;
    y1 = y1 * CANVAS_SCALE_FACTOR; 
    //TODO:Pretty sure the zoom broken here
    if(g_state.zoom_mode==ZOOM_MODE_IN)
    {
        scale = 1.0f / ZOOM_SCALE;
        x0 = (scale * x0) + g_state.zoom_rect.x; 
        x1 = (scale * x1) + g_state.zoom_rect.x;
        y0 = (scale * y0) + g_state.zoom_rect.y; 
        y1 = (scale * y1) + g_state.zoom_rect.y;
    }
    //draws the line on a virual texture that wond be visible until the render() function
    //set_render_target(ap_renderer, g_state.drawing_texture); 
    draw_textured_line(ap_renderer, g_state.brush_texture, x0, y0, x1, y1, BRUSH_W, BRUSH_H);
//    SDL_RenderDrawLine(ap_renderer, x0, y0, x1, y1);
    g_state.xmo = xm; 
    g_state.ymo = ym;
}

void setup(SDL_Renderer *ap_renderer)
{
    //set the renderers blend mode to make sure transparency works
    SDL_SetRenderDrawBlendMode(ap_renderer, SDL_BLENDMODE_BLEND);
    //these variables control how textures are created
    uint32_t fmt = SDL_PIXELFORMAT_RGBA32;
    int access = SDL_TEXTUREACCESS_TARGET;
//    /*
//     * setup the global drawing texture. possible could create a canvas struct if it makes thigs easier
//    */
    g_state.drawing_texture = SDL_CreateTexture(ap_renderer, fmt, access, CANVAS_WIDTH*CANVAS_SCALE_FACTOR, CANVAS_HEIGHT*CANVAS_SCALE_FACTOR); 
    if(g_state.drawing_texture==NULL)
    {
        printf("Error Creating Drawing texture: %s\n", SDL_GetError());
    }
    SDL_SetTextureBlendMode(g_state.drawing_texture, SDL_BLENDMODE_BLEND); 
    SDL_SetTextureBlendMode(g_state.drawing_texture, SDL_BLENDMODE_BLEND); 
    set_render_target(ap_renderer, g_state.drawing_texture);
    set_render_draw_color(ap_renderer, C_ALPHA);
    SDL_RenderClear(ap_renderer);
    SDL_Texture *paper_texture;
    paper_texture = load_texture_form_path(ap_renderer, "./assets/drawing_texture.png"); 
    SDL_RenderCopy(ap_renderer, paper_texture, NULL, NULL);  
    SDL_DestroyTexture(paper_texture);
    /*
     * Setup the global grid texture, could make a grid struct for neatness 
    */
    g_state.grid_texture = SDL_CreateTexture(ap_renderer, fmt, access, CANVAS_WIDTH, CANVAS_HEIGHT); 
    if(g_state.grid_texture==NULL)
    {
        printf("Error Creating Border texture: %s\n", SDL_GetError());
    }
    SDL_SetTextureBlendMode(g_state.grid_texture, SDL_BLENDMODE_BLEND); 
    set_render_target(ap_renderer, g_state.grid_texture);
    set_render_draw_color(ap_renderer, C_ALPHA);
    SDL_RenderClear(ap_renderer);
    set_render_draw_color(ap_renderer, C_GREY2);
    draw_grid(ap_renderer, GRID_SIZE);
    /*
     * Setup the Brush texture
    */
    g_state.brush_texture = load_texture_form_path(ap_renderer, "./assets/b0.png"); 
    SDL_SetTextureBlendMode(g_state.brush_texture, SDL_BLENDMODE_BLEND); 
    /*
     * Setup the Backround texture
    */
    g_state.backround_texture = load_texture_form_path(ap_renderer, "./assets/bkgnd.png");
    /*
     * Setup the Refrence Texture
    */
    g_state.refrence_texture= SDL_CreateTexture(ap_renderer, fmt, access, REFRENCE_SCREEN_WIDTH, REFRENCE_SCREEN_HEIGHT); 
    if(g_state.refrence_texture==NULL)
    {
        printf("Error Creating refrecne texture: %s\n", SDL_GetError());
    }
    SDL_SetTextureBlendMode(g_state.refrence_texture, SDL_BLENDMODE_BLEND); 
    set_render_target(ap_renderer, g_state.refrence_texture);
    set_render_draw_color(ap_renderer, C_ALPHA);
    SDL_RenderClear(ap_renderer);
    SDL_Texture *temp_tex = load_texture_form_path(ap_renderer, "./assets/ref_test.png");
    int w, h;
    SDL_QueryTexture(temp_tex, NULL, NULL, &w, &h);
    SDL_Rect dest;
    dest.x =0; dest.y = 0;
    dest.w = REFRENCE_SCREEN_WIDTH; 
    dest.h = REFRENCE_SCREEN_HEIGHT;
    //possible test differnt scale modes here
    SDL_RenderCopy(ap_renderer, temp_tex, NULL, &dest); 
    SDL_DestroyTexture(temp_tex);
    /*
     * Setp the rest of the global variables, may want to rething things since there are a lot of these...
    */
    g_state.tool_type = TOOL_2H_PENCIL;
    g_state.zoom_mode = ZOOM_MODE_OUT;
    g_state.grid_mode = GRID_MODE_OFF;
    g_state.tool_width = WIDTH_MODE_THIN;
    g_state.scoll_direction = SCROLL_DIR_NONE;
    g_state.pen_down = false;
    g_state.xmo = 0;
    g_state.ymo = 0;
    g_state.zoom_rect.x = 0;
    g_state.zoom_rect.y = 0;
    g_state.zoom_rect.w = CANVAS_WIDTH / ZOOM_SCALE;
    g_state.zoom_rect.h = CANVAS_HEIGHT / ZOOM_SCALE;
    g_state.ref_mode = REF_MODE_DRAW;
    //set the render target back to default
    set_render_target(ap_renderer, NULL);
}

void update(SDL_Renderer *ap_renderer, SDL_Event *e, float delta_time)
{
    if(e==0){return;}//just return if there was no input this frame
    if(e->type==SDL_KEYUP)
    {
        switch(e->key.keysym.sym)
        {
            case SDLK_TAB:
               g_state.tool_width = !g_state.tool_width; 
               break;
            case SDLK_1:
               printf("selecting 2h pencil\n");
               g_state.tool_type = TOOL_2H_PENCIL; 
               break;
            case SDLK_2:
               printf("selecting hb pencil\n");
               g_state.tool_type = TOOL_HB_PENCIL; 
               break;
            case SDLK_3:
               printf("Selecting 2b pencil\n");
               g_state.tool_type = TOOL_2B_PENCIL; 
               break;
            case SDLK_e:
               printf("Selecting Eraser\n");
               g_state.tool_type = TOOL_ERASER; 
               break;
            case SDLK_g:
               g_state.grid_mode = !g_state.grid_mode; 
               break;
            case SDLK_z:
               g_state.zoom_mode = !g_state.zoom_mode; 
               break;
            case SDLK_w:
               g_state.scoll_direction = SCROLL_DIR_NONE;
               break;
            case SDLK_s:
               g_state.scoll_direction = SCROLL_DIR_NONE;
               break;
            case SDLK_a:
               g_state.scoll_direction = SCROLL_DIR_NONE;
               break;
            case SDLK_d:
               g_state.scoll_direction = SCROLL_DIR_NONE;
               break;
            case SDLK_r:
               g_state.ref_mode = !g_state.ref_mode;
               break;
        }
    }
    else if(e->type == SDL_KEYDOWN & g_state.zoom_mode == ZOOM_MODE_IN)
    {
        int scaled_canvas_h = CANVAS_HEIGHT*CANVAS_SCALE_FACTOR;
        int scaled_canvas_w = CANVAS_WIDTH*CANVAS_SCALE_FACTOR;
        switch(e->key.keysym.sym)
        {
            case SDLK_s:
               g_state.scoll_direction = SCROLL_DIR_UP;
               g_state.zoom_rect.y += SCROLL_SPEED;
               if (g_state.zoom_rect.y + scaled_canvas_h/ZOOM_SCALE > scaled_canvas_h)
               {
                   g_state.zoom_rect.y = scaled_canvas_h/ZOOM_SCALE;
               }
               break;
            case SDLK_w:
               g_state.scoll_direction = SCROLL_DIR_DOWN;
               g_state.zoom_rect.y -= SCROLL_SPEED;
               if (g_state.zoom_rect.y < 0)
               {
                   g_state.zoom_rect.y = 0;
               }
               break;
            case SDLK_a:
               g_state.scoll_direction = SCROLL_DIR_LEFT;
               g_state.zoom_rect.x -= SCROLL_SPEED;
               if (g_state.zoom_rect.x < 0)
               {
                   g_state.zoom_rect.x = 0;
               }
               break;
            case SDLK_d:
               g_state.scoll_direction = SCROLL_DIR_RIGHT;
               g_state.zoom_rect.x += SCROLL_SPEED;
               if (g_state.zoom_rect.x+scaled_canvas_w/ZOOM_SCALE > scaled_canvas_w)
               {
                   g_state.zoom_rect.x = scaled_canvas_w/ZOOM_SCALE;
               }
               break;
        }
    }
    else if(e->type==SDL_MOUSEBUTTONDOWN)
    {
        if(point_is_in_draw_area(e->button.x, e->button.y))
        {
            g_state.pen_down = true;
            g_state.xmo = e->button.x;
            g_state.ymo = e->button.y;
        }
    }
    else if(e->type==SDL_MOUSEBUTTONUP)
    {
        g_state.pen_down = false;
    }
}

void render(SDL_Renderer *ap_renderer)
{
    //render to the draw texture with pencil stokes
    if(g_state.pen_down)
    {
        set_render_target(ap_renderer, g_state.drawing_texture);
        draw_pen_stroke(ap_renderer);
    }
    //render the textures to the main window
    set_render_target(ap_renderer, NULL);
    //render the backround/border first
    SDL_Rect dest_rect;
    dest_rect.x = REFRENCE_SCREEN_X;
    dest_rect.y = REFRENCE_SCREEN_Y;
    dest_rect.w = REFRENCE_SCREEN_WIDTH; 
    dest_rect.h = REFRENCE_SCREEN_HEIGHT;
    set_render_draw_color(ap_renderer, C_WHITE);
    SDL_RenderClear(ap_renderer);
    SDL_RenderCopy(ap_renderer, g_state.backround_texture, NULL, NULL);
    //SDL_RenderCopy(ap_renderer, g_state.border_texture, NULL, NULL);
    //render the top screen second
    if((g_state.ref_mode == REF_MODE_IMG) & (g_state.refrence_texture != NULL))
    {
        SDL_RenderCopy(ap_renderer, g_state.refrence_texture, NULL, &dest_rect);
    }
    else
    {
        SDL_RenderCopy(ap_renderer, g_state.drawing_texture, NULL, &dest_rect);
    }
    if(g_state.grid_mode == GRID_MODE_ON)
    {
        SDL_RenderCopy(ap_renderer, g_state.grid_texture, NULL, &dest_rect);
    }
    //render the drawing_texture. Scale it down first
    dest_rect.x = CANVAS_X;
    dest_rect.y = CANVAS_Y;
    dest_rect.w = CANVAS_WIDTH;
    dest_rect.h = CANVAS_HEIGHT;
    g_state.zoom_rect.x = g_state.zoom_rect.x;
    g_state.zoom_rect.y = g_state.zoom_rect.y;
    g_state.zoom_rect.w = CANVAS_WIDTH*CANVAS_SCALE_FACTOR;
    g_state.zoom_rect.h = CANVAS_HEIGHT*CANVAS_SCALE_FACTOR;
    if(g_state.zoom_mode == ZOOM_MODE_IN)
    {
          g_state.zoom_rect.w = g_state.zoom_rect.w/ZOOM_SCALE;
          g_state.zoom_rect.h = g_state.zoom_rect.h/ZOOM_SCALE;
    }
    SDL_RenderCopy(ap_renderer, g_state.drawing_texture, &g_state.zoom_rect, &dest_rect);
    //render the grid over the canvas
    SDL_Rect grid_zoom_rect;
    grid_zoom_rect.x = g_state.zoom_rect.x / CANVAS_SCALE_FACTOR;
    grid_zoom_rect.y = g_state.zoom_rect.y / CANVAS_SCALE_FACTOR;
    grid_zoom_rect.w = CANVAS_WIDTH;
    grid_zoom_rect.h = CANVAS_HEIGHT;
    if(g_state.zoom_mode == ZOOM_MODE_IN)
    {
          grid_zoom_rect.w = (CANVAS_WIDTH)/ZOOM_SCALE;
          grid_zoom_rect.h = (CANVAS_HEIGHT)/ZOOM_SCALE;
    }
    if(g_state.grid_mode == GRID_MODE_ON)
    {
        SDL_RenderCopy(ap_renderer, g_state.grid_texture, &grid_zoom_rect, &dest_rect);
    }
    //render the cursor last on top of everything else
    int cr = 24;
    if(g_state.pen_down){cr=12;}
    draw_cursor(ap_renderer, cr, C_BLACK, C_GREY2);
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
    update(ap_renderer, &e, delta_time);
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
  int sdl_initilized = initilizeSdl(&main_window, &main_renderer, WINDOW_WIDTH, WINDOW_HEIGHT);
  if(!sdl_initilized)
  {
      printf("SDL Setup Failed\n");
      return -1;
  }
  setup(main_renderer);
  if(!SDL_RenderTargetSupported(main_renderer))
  {
      printf("The main renderer does not support rendering to targets...\n");
      return -1;
  }
  printf("Full Screen Size= %dx%d px\n", WINDOW_WIDTH, WINDOW_HEIGHT);
  printf("Bottom Screen Rect x,y=%d,%d w,h=%d,%d\n", CANVAS_X, CANVAS_Y, CANVAS_WIDTH, CANVAS_HEIGHT);
  printf("Top Screen Rect x,y=%d,%d w,h=%d,%d\n", REFRENCE_SCREEN_X, REFRENCE_SCREEN_Y, REFRENCE_SCREEN_WIDTH, REFRENCE_SCREEN_HEIGHT);
  main_loop(main_renderer);
  //destroy everything
  SDL_DestroyTexture(g_state.drawing_texture);
  SDL_DestroyTexture(g_state.grid_texture);
  SDL_DestroyTexture(g_state.backround_texture);
  SDL_DestroyTexture(g_state.refrence_texture);
  SDL_DestroyTexture(g_state.brush_texture);
  SDL_DestroyRenderer(main_renderer);
  SDL_DestroyWindow(main_window);
  TTF_Quit();
  Mix_Quit();
  SDL_Quit();
  return 0;
}
