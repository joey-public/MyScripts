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

int render(Paddle a_paddle, Ball a_ball, SDL_Renderer* a_renderer, ColorPallete a_pallete)
{
    int return_val = TRUE;
    SDL_Color bg_color = a_pallete.c1;//darkest color
    SDL_SetRenderDrawColor(a_renderer, bg_color.r, bg_color.g, bg_color.b, bg_color.a);
    SDL_Rect background = {0,0,SCREEN_WIDTH, SCREEN_HEIGHT};
    SDL_RenderFillRect(a_renderer, &background);
    return_val &= paddleRender(a_paddle, a_renderer, a_pallete);
    return_val &= ballRender(a_ball, a_renderer, a_pallete);
    //start text rendering, gotta move this out of here 
    TTF_Font* test_font;
    int font_size = 28;
    test_font = TTF_OpenFont("./assests/instruction/Instruction.ttf", font_size); 
    SDL_Surface* test_surface = TTF_RenderText_Solid(test_font, "Hello!", a_pallete.c2); 
    if(test_surface==NULL){
      printf( "Unable to render text surface! SDL_ttf Error: %s\n", TTF_GetError() );
    }
    SDL_Texture* test_texture = SDL_CreateTextureFromSurface(a_renderer, test_surface);
    if(test_texture==NULL){
      printf( "Unable to create texture from rendered text! SDL Error: %s\n", SDL_GetError() );
    }
    SDL_FreeSurface(test_surface);
    SDL_Color text_color = a_pallete.c2;//darkest color
    SDL_SetRenderDrawColor(a_renderer, text_color.r, text_color.g, text_color.b, text_color.a);
    SDL_RenderCopy(a_renderer, test_texture, NULL, NULL);
    //end text rendering 
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
  ColorPallete main_pallete = setupColorPallete();
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
        game_is_running &= render(main_paddle, main_ball, main_renderer, main_pallete);
        current_game_state = play;
        break;
      case play:
        game_is_running &= processInput(&game_input_state); 
        game_is_running &= update(&main_paddle, &main_ball, main_audio_player, game_input_state, &score, delta_time);
        game_is_running &= render(main_paddle, main_ball, main_renderer, main_pallete);
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
        game_is_running &= render(main_paddle, main_ball, main_renderer, main_pallete);
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
  TTF_Quit();
  Mix_Quit();
  SDL_Quit();
  printf("Thansks for playing :)\n");
  return 0;
}
