#include <stdio.h>
#include <time.h>
#include <stdlib.h>
#include <SDL2/SDL.h>
#include <SDL2/SDL_mixer.h>
#include <SDL2/SDL_ttf.h>
#include "./include/custom_types.h"
#include "./include/init_sdl.h"
#include "./include/input_handler.h"
#include "./include/paddle.h"
#include "./include/ball.h"
#include "./include/constants.h"
#include "./include/audio_player.h"
#include "./include/score_keeper.h"

//#define USE_EMSCRIPTEN

#ifdef USE_EMSCRIPTEN
  #define FPS 30
  #define EM_INF_LOOP 1
  #include <emscripten.h>
#endif

                                                 
typedef struct MainLoopArgs {
  SDL_Window* window;
  SDL_Renderer* renderer;
  AudioPlayer audio_player;
  GameInputState game_input_state;
  ColorPallete color_pallete;
  ScoreKeeper score_keeper;
  Ball ball;
  Paddle paddle;
  float delta_time;
  int game_is_running; 
  int current_game_state;
  
}MainLoopArgs;

ColorPallete setupColorPallete()
{
  ColorPallete p;
  p.c0.r = 55;  p.c0.g = 86;  p.c0.b = 32; p.c0.a = 255;
  p.c1.r = 109; p.c1.g = 142; p.c1.b = 52; p.c1.a = 255;
  p.c2.r = 129; p.c2.g = 183; p.c2.b = 12; p.c2.a = 255;
  p.c3.r = 205; p.c3.g = 219; p.c3.b = 87; p.c3.a = 255;
  return p;
}

int check_paddle_ball_colision(Paddle a_paddle, Ball a_ball)
{
  SDL_Rect r1 = a_ball.sprite_box;
  SDL_Rect r2 = a_paddle.sprite_box;
  int x_overlap = ((r1.x+r1.w) > r2.x) & (r1.x < (r2.x+r2.w));
  int y_overlap = ((r1.y+r1.h) > r2.y) & (r1.y < (r2.y+r2.h));
  return (x_overlap & y_overlap);
}

//return TRUE if the game should be played or False if its game over
int update(Paddle* a_paddle, Ball* a_ball, ScoreKeeper* a_score_keeper, AudioPlayer a_audio_player, GameInputState a_input_state, float a_delta_time, SDL_Renderer* a_renderer, ColorPallete a_pallete)
{
  paddleUpdate(a_paddle, a_input_state, a_delta_time);
  ballUpdate(a_ball, *a_paddle, a_audio_player, a_delta_time);
  scoreKeeperUpdate(a_score_keeper, a_delta_time, a_renderer, a_pallete);
  //Handle Collisions between ball and paddle here
  if(check_paddle_ball_colision(*a_paddle, *a_ball)){
    Mix_PlayChannel(-1, a_audio_player.sound_ball_paddle_collision, 0);
    a_ball->y_position = PADDLE_Y_POS-BALL_HEIGHT;
    a_ball->y_velocity = -1 * a_ball->y_velocity;
    a_score_keeper->score ++;
  }
  return TRUE;
}

int render(Paddle a_paddle, Ball a_ball, ScoreKeeper a_score_keeper, ColorPallete a_pallete, SDL_Renderer* a_renderer)
{
    int return_val = TRUE;
    SDL_Color bg_color = a_pallete.c1;//darkest color
    SDL_SetRenderDrawColor(a_renderer, bg_color.r, bg_color.g, bg_color.b, bg_color.a);
    SDL_Rect background = {0,0,SCREEN_WIDTH, SCREEN_HEIGHT};
    SDL_RenderFillRect(a_renderer, &background);
    return_val &= paddleRender(a_paddle, a_renderer, a_pallete);
    return_val &= ballRender(a_ball, a_renderer, a_pallete);
    return_val &= scoreKeeperRender(a_score_keeper, a_renderer, a_pallete);
    SDL_RenderPresent(a_renderer);
    return return_val;
}

void main_loop_iter(void* a)
{
  MainLoopArgs* args = a;
  const int START = 0;
  const int PLAY = 1;
  const int STOP = 2;
  if(args->current_game_state == START){
    SDL_Delay(250);//chill for 250 ms
    ballSetup(&(args->ball));
//    args->score_keeper = scoreKeeperSetup(args->renderer, args->color_pallete);
    args->game_is_running &= render(args->paddle, args->ball, args->score_keeper , args->color_pallete,args->renderer);
    args->current_game_state = PLAY;
  }
  else if (args->current_game_state == PLAY){
    args->game_is_running &= processInput(&(args->game_input_state)); 
    args->game_is_running &= update(&(args->paddle), &(args->ball), &(args->score_keeper), 
                              args->audio_player, args->game_input_state, 
                              args->delta_time, args->renderer, args->color_pallete);
    args->game_is_running &= render(args->paddle, args->ball, args->score_keeper , args->color_pallete,args->renderer);
    //Handle the Game Case here:
    int bottom_wall_collision = args->ball.y_position > SCREEN_HEIGHT-BALL_HEIGHT;//this collision is sometimes broken...
    if(bottom_wall_collision){ 
        printf("You Lose\n");
        args->current_game_state=STOP;
    }
  }
  else{
    SDL_Delay(250);//chill for 250 ms
    args->game_is_running &= render(args->paddle, args->ball, args->score_keeper, args->color_pallete,args->renderer);
    (args->score_keeper).score = 0;
    SDL_Delay(250);//chill for 250 ms
    args->current_game_state = START;
  }
}

void main_loop(MainLoopArgs* args)
{
  args->game_is_running = TRUE;
  int last_frame_time = SDL_GetTicks();
  args->current_game_state = 0;
  while(args->game_is_running){
    //while(!SDL_TICKS_PASSED(SDL_GetTicks(), last_frame_time+FRAME_TARGET_TIME)); 
    int wait_time = FRAME_TARGET_TIME - (SDL_GetTicks() - last_frame_time);
    if(wait_time > 0 && wait_time <= FRAME_TARGET_TIME){
        SDL_Delay(wait_time);
    }
    args->delta_time = (SDL_GetTicks() - last_frame_time) / 1000.0f;
    last_frame_time = SDL_GetTicks();//look this up
    main_loop_iter(args);
  }//end while loop
}//end function

int main( int argc, char* args[] )
{
  srand(time(NULL));
  //initalize sdl stuff
  MainLoopArgs loop_args;
  loop_args.window = NULL;
  loop_args.renderer = NULL;
  int sdl_initilized = FALSE;
  sdl_initilized = init(&(loop_args.window), &(loop_args.renderer));
  if (!sdl_initilized){
    printf("SDL Setup Failed\n");
    return -1;
  }
  loop_args.audio_player = audioPlayerSetup();
  loop_args.game_input_state = gameInputStateSetup();
  loop_args.color_pallete = setupColorPallete();
  loop_args.score_keeper = scoreKeeperSetup(loop_args.renderer, loop_args.color_pallete);
  loop_args.ball = ballCreate();
  loop_args.paddle = paddleSetup();
  loop_args.delta_time = 0.0f;
  loop_args.game_is_running = FALSE;
  loop_args.current_game_state = 0;
//#ifdef USE_EMSCRIPTEN 
//  emscripten_set_main_loop_arg(main_loop_iter, &loop_args, FPS, EM_INF_LOOP);
//#else
  main_loop(&loop_args);
//#endif

  //destroy everything
  audioPlayerDestroy(&(loop_args.audio_player));
  scoreKeeperDestroy(&(loop_args.score_keeper));
  SDL_DestroyRenderer(loop_args.renderer);
  SDL_DestroyWindow(loop_args.window);
  TTF_Quit();
  Mix_Quit();
  SDL_Quit();
  printf("Thansks for playing :)\n");
  return 0;
}
