#include <stdio.h>
#include <time.h>
#include <stdlib.h>
#include <SDL2/SDL.h>
#include <SDL2/SDL_mixer.h>
#include "./include/custom_types.h"
#include "./include/init_sdl.h"
#include "./include/input_handler.h"
#include "./include/paddle.h"
#include "./include/ball.h"
#include "./include/constants.h"
#include "./include/audio_player.h"
                                                 


int check_paddle_ball_colision(Paddle a_paddle, Ball a_ball)
{
  SDL_Rect r1 = a_ball.sprite_box;
  SDL_Rect r2 = a_paddle.sprite_box;
  int x_overlap = ((r1.x+r1.w) > r2.x) & (r1.x < (r2.x+r2.w));
  int y_overlap = ((r1.y+r1.h) > r2.y) & (r1.y < (r2.y+r2.h));
  return (x_overlap & y_overlap);
}

//return TRUE if the game should be played or False if its game over
int update(Paddle* a_paddle, Ball* a_ball, AudioPlayer a_audio_player, GameInputState a_input_state, int* a_score, float a_delta_time)
{
  paddleUpdate(a_paddle, a_input_state, a_delta_time);
  ballUpdate(a_ball, *a_paddle, a_audio_player, a_delta_time);
  //Handle Collisions between ball and paddle here
  if(check_paddle_ball_colision(*a_paddle, *a_ball)){
    Mix_PlayChannel(-1, a_audio_player.sound_ball_paddle_collision, 0);
    a_ball->y_position = PADDLE_Y_POS-BALL_HEIGHT;
    a_ball->y_velocity = -1 * a_ball->y_velocity;
    (*a_score) ++;
  }
  return TRUE;
}

int render(Paddle a_paddle, Ball a_ball, SDL_Renderer* a_renderer)
{
    int return_val = TRUE;
    SDL_SetRenderDrawColor(a_renderer, 255, 255, 255, 255);
    SDL_Rect background = {0,0,SCREEN_WIDTH, SCREEN_HEIGHT};
    SDL_RenderFillRect(a_renderer, &background);
    return_val &= paddleRender(a_paddle, a_renderer);
    return_val &= ballRender(a_ball, a_renderer);
    SDL_RenderPresent(a_renderer);
    return return_val;
}

int main( int argc, char* args[] )
{
  srand(time(NULL));
  SDL_Window* main_window = NULL;
  SDL_Renderer* main_renderer = NULL;
  int game_is_running = 1;
  int last_frame_time = SDL_GetTicks();
  int score = 0;
  float delta_time = 0.0f;
  game_is_running = init(&main_window, &main_renderer);
  enum states {start, play, stop};
  enum states current_game_state = start;
  if (!game_is_running){
    printf("SDL Setup Failed\n");
    return -1;
  }
  //main loop
  AudioPlayer main_audio_player = audioPlayerSetup();
  Paddle main_paddle = paddleSetup();
  Ball main_ball = ballSetup();
  GameInputState game_input_state = gameInputStateSetup();
 
  while(game_is_running){
    //while(!SDL_TICKS_PASSED(SDL_GetTicks(), last_frame_time+FRAME_TARGET_TIME)); 
    int wait_time = FRAME_TARGET_TIME - (SDL_GetTicks() - last_frame_time);
    if(wait_time > 0 && wait_time <= FRAME_TARGET_TIME){
        SDL_Delay(wait_time);
    }
    delta_time = (SDL_GetTicks() - last_frame_time) / 1000.0f;
    last_frame_time = SDL_GetTicks();//look this up
                                     
    switch(current_game_state)
    {
      case start:
        SDL_Delay(250);//chill for 250 ms
        current_game_state = play;
        main_ball=ballSetup();
        main_paddle=paddleSetup();
        game_is_running &= render(main_paddle, main_ball, main_renderer);
        current_game_state = play;
        break;
      case play:
        game_is_running &= processInput(&game_input_state); 
        game_is_running &= update(&main_paddle, &main_ball, main_audio_player, game_input_state, &score, delta_time);
        game_is_running &= render(main_paddle, main_ball, main_renderer);
        //Handle the Game Case here:
        int bottom_wall_collision = main_ball.y_position > SCREEN_HEIGHT-BALL_HEIGHT;//this collision is sometimes broken...
        if(bottom_wall_collision){ 
            printf("You Lose\n");
            current_game_state=stop;
        }
        //printf("Score: %d\n", score);
        break;
      case stop:
        SDL_Delay(250);//chill for 250 ms
        main_ball=ballSetup();
        main_paddle=paddleSetup();
        game_is_running &= render(main_paddle, main_ball, main_renderer);
        SDL_Delay(250);//chill for 250 ms
        score = 0;
        current_game_state = play;
        break;
    }
  }
  //destroy everything
  destroyAudioPlayer(&main_audio_player);
  SDL_DestroyRenderer(main_renderer);
  SDL_DestroyWindow(main_window);
  SDL_Quit();
  printf("Thansks for playing :)\n");
  return 0;
}
